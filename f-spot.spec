%define name 	f-spot
%define version	0.4.0
%define release	%mkrel 6

Summary:	A full-featured personal photo management application for the GNOME desktop
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch:		f-spot-0.3.2-dllmap.patch
Patch1:		f-spot-0.4.0-sqlite3-update.patch
# gw: Ubuntu patch with several fixes from svn:
# b.g.o #463789 b.g.o #462939 b.g.o #462069 bgo #464981 bgo #463690 novell bug #304124
Patch2: 	f-spot-0.4.0-svnfixes.patch
License:	GPLv2+
Group: 		Graphics
Url:		http://f-spot.org
BuildRequires:  intltool
BuildRequires:	gnome-sharp2 >= 2.8.0
BuildRequires:	mono-devel
BuildRequires:	mono-data-sqlite
BuildRequires:	libgnomeui2-devel
BuildRequires:	libexif-devel
BuildRequires:	lcms-devel
BuildRequires:	sqlite-devel
BuildRequires:	libgphoto-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	scrollkeeper
BuildRequires:	gnome-doc-utils
BuildRequires:	libxslt-proc
BuildRequires:	ndesk-dbus-glib
#gw this is needed for automatic mono deps
BuildRequires:	libmesaglu-devel
#gw required for the upgrade script
Requires:	sqlite-tools
Requires:	sqlite3-tools
#gw please don't drop these explicit deps, the shared libraries are imported
Requires:	%mklibname exif 12
Requires:	%mklibname gphoto 2
Requires(post): shared-mime-info scrollkeeper
Requires(postun): shared-mime-info scrollkeeper
#gw workaround for urpmi bug 29356
%define _provides_exceptions mono.libgphoto2-sharp
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
F-Spot is a full-featured personal photo management application
for the GNOME desktop.

Features:
* Simple user interface
* Photo editor
* Color adjustments
* Tag icon editor
* Create photo cd
* Export to web

%prep
%setup -q
%patch -p1 -b .dllmap
%patch1 -p1 -b .sqlite3-update
%patch2 -p1 -b .svnfixes

#needed by patch2
intltoolize --copy --force
autoreconf

%build
%configure2_5x \
	--disable-scrollkeeper \
	--disable-static
%make

%install
rm -rf %{buildroot} %name.lang
%makeinstall_std saverdir=%_libdir/gnome-screensaver/
rm -f %buildroot%_libdir/%name/libfspot*a

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done


mkdir -p %buildroot{%_liconsdir,%_miconsdir}
ln -s %_datadir/icons/hicolor/48x48/apps/%name.png %buildroot%_liconsdir/%name.png
ln -s %_datadir/icons/hicolor/32x32/apps/%name.png %buildroot%_iconsdir/%name.png
ln -s %_datadir/icons/hicolor/16x16/apps/%name.png %buildroot%_miconsdir/%name.png

%clean
rm -rf %{buildroot}

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
%_iconsdir/hicolor/*/*/*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
