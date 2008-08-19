%define name 	f-spot
%define version	0.4.4
%define release	%mkrel 3

Summary:	A full-featured personal photo management application for the GNOME desktop
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch:		f-spot-0.3.2-dllmap.patch
Patch1:		f-spot-0.4.2-sqlite3-update.patch
Patch2:		f-spot-0.4.4-deprecated.patch
Patch3: f-spot-0.4.2-no-multiple-files-in-viewer.patch
License:	GPLv2+
Group: 		Graphics
Url:		http://f-spot.org
BuildRequires:  intltool
%if %mdvver >= 200900
BuildRequires:	gnome-sharp2-devel >= 2.8.0
BuildRequires:	gnome-desktop-sharp-devel
%else
BuildRequires:	gnome-sharp2 >= 2.8.0
BuildRequires:	gnome-desktop-sharp
%endif
BuildRequires:	beagle
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
%define _provides_exceptions mono.libgphoto2-sharp\\|mono.Mono.Addins\\|mono.gnome-keyring-sharp
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
%patch2 -p1
%patch3 -p1
intltoolize --force
aclocal
autoconf
automake

%build
#gw TODO: fix build without this
%define _disable_ld_no_undefined 1
%configure2_5x \
	--disable-scrollkeeper \
	--disable-static
#gw, parallel make fails in 0.4.4
make

%install
rm -rf %{buildroot} %name.lang
%makeinstall saverdir=%buildroot%_libdir/gnome-screensaver/ plugindir=%buildroot%_libdir/f-spot/extensions themesdir=%buildroot%_datadir/applications/screensavers

rm -f %buildroot%_libdir/%name/libfspot*a

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%update_scrollkeeper
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%clean_scrollkeeper
%clean_desktop_database
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS MAINTAINERS NEWS README TODO
%_bindir/%name
%_bindir/%name-import
%_bindir/%name-sqlite-upgrade
%dir %_libexecdir/gnome-screensaver/
%_libexecdir/gnome-screensaver/f-spot-screensaver
%_libdir/%name
%_datadir/applications/%name.desktop
%_datadir/applications/%name-import.desktop
%_datadir/applications/%name-view.desktop
%_datadir/applications/screensavers/f-spot-screensaver.desktop
%dir %_datadir/omf/*/
%_datadir/omf/*/*-C.omf
%_libdir/pkgconfig/*.pc
%_libdir/gio-sharp-unstable
%_datadir/f-spot
%_iconsdir/hicolor/*/*/*
