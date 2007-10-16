%define name 	f-spot
%define version	0.4.0
%define release	%mkrel 4

Summary: 	A full-featured personal photo management application for the GNOME desktop
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch: f-spot-0.3.2-dllmap.patch
Patch1: f-spot-0.4.0-sqlite3-update.patch
License: 	GPL
Group: 		Graphics
Url: 		http://f-spot.org/
BuildRequires: 	gnome-sharp2 >= 2.8.0
BuildRequires: 	mono-devel
BuildRequires: 	mono-data-sqlite
BuildRequires: 	libgnomeui2-devel
BuildRequires: 	libexif-devel
BuildRequires: 	lcms-devel
BuildRequires: 	sqlite-devel
BuildRequires: 	libgphoto-devel
BuildRequires: 	perl-XML-Parser
BuildRequires: 	desktop-file-utils
BuildRequires: 	scrollkeeper gnome-doc-utils libxslt-proc
BuildRequires: 	ndesk-dbus-glib
#gw this is needed for automatic mono deps
BuildRequires: libmesaglu-devel
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
#gw required for the upgrade script
Requires: sqlite-tools sqlite3-tools
#gw please don't drop these explicit deps, the shared libraries are imported
Requires: 	%mklibname exif 12
Requires: 	%mklibname gphoto 2
Requires(post): shared-mime-info scrollkeeper
Requires(postun): shared-mime-info scrollkeeper
#gw workaround for urpmi bug 29356
%define _provides_exceptions mono.libgphoto2-sharp

%description
F-Spot is a full-featured personal photo management application
for the GNOME desktop

%prep
%setup -q
%patch -p1 -b .dllmap
%patch1 -p1 -b .sqlite3-update
cp %_prefix/lib/mono/ndesk-dbus-1.0/*.dll dbus-sharp
cp %_prefix/lib/mono/ndesk-dbus-glib-1.0/*.dll dbus-sharp-glib

%build
%configure2_5x --disable-scrollkeeper
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std saverdir=%_libdir/gnome-screensaver/
rm -f %buildroot%_libdir/%name/libfspot*a
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Photograph" \
  --add-category="X-MandrivaLinux-Multimedia-Graphics" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*



%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done


mkdir -p %buildroot{%_liconsdir,%_miconsdir}
ln -s %_datadir/icons/hicolor/48x48/apps/%name.png %buildroot%_liconsdir/%name.png
ln -s %_datadir/icons/hicolor/32x32/apps/%name.png %buildroot%_iconsdir/%name.png
ln -s %_datadir/icons/hicolor/16x16/apps/%name.png %buildroot%_miconsdir/%name.png

#gw now in external package
rm -f %buildroot%_libdir/f-spot/NDesk.DBus*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_icon_cache hicolor
%update_scrollkeeper
%update_desktop_database

%postun
%clean_menus
%clean_icon_cache hicolor
%clean_scrollkeeper
%clean_desktop_database

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%_bindir/%name
%_bindir/%name-import
%_bindir/%name-sqlite-upgrade
%dir %_libexecdir/gnome-screensaver/
%_libexecdir/gnome-screensaver/f-spot-screensaver
%_libdir/%name
%_datadir/applications/%name.desktop
%_datadir/applications/%name-view.desktop
%_datadir/gnome-screensaver/
%dir %_datadir/omf/*/
%_datadir/omf/*/*-C.omf
%_libdir/pkgconfig/*.pc
%_datadir/f-spot
%_datadir/icons/hicolor/*/*/*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
