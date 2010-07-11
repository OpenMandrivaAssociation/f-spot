%define name 	f-spot
%define version	0.6.2
%define release	%mkrel 1

Summary:	A full-featured personal photo management application for the GNOME desktop
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch:		f-spot-0.3.2-dllmap.patch
Patch1:		f-spot-0.5.0.3-sqlite3-update.patch
Patch3: f-spot-0.6.1.3-no-multiple-files-in-viewer.patch
# (fc) 0.4.4-4mdv use system gnome-keyring-sharp (Debian)
Patch6:		f-spot-0.6.2-gnome-keyring-sharp.patch
# (fc) 0.4.4-4mdv fix underlinking (Debian)
Patch7:		f-spot-0.6.0.0-fixunderlinking.patch
# (fc) 0.5.0.3-3mdv fix string format error
Patch8:		f-spot-0.5.0.3-str_fmt.patch
License:	GPLv2+
Group: 		Graphics
Url:		http://f-spot.org
BuildRequires:  intltool
%if %mdvver >= 200900
BuildRequires:	gnome-sharp2-devel >= 2.8.0
BuildRequires:	gnome-desktop-sharp-devel
BuildRequires:  gnome-keyring-sharp
%else
BuildRequires:	gnome-sharp2 >= 2.8.0
BuildRequires:	gnome-desktop-sharp
%endif
BuildRequires:  libGConf2-devel
BuildRequires:  libgnomeui2-devel
BuildRequires:	mono-devel
BuildRequires:	mono-data-sqlite
BuildRequires:	mono-addins
BuildRequires:	libexif-devel
BuildRequires:	lcms-devel
BuildRequires:	sqlite-devel
BuildRequires:	libgphoto-devel
BuildRequires:	unique-devel
BuildRequires:	scrollkeeper
BuildRequires:	gnome-doc-utils
BuildRequires:	libxslt-proc
BuildRequires:	ndesk-dbus-glib
BuildRequires:  gnome-screensaver
BuildRequires:  gettext-devel
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
%define _provides_exceptions mono.libgphoto2-sharp\\|mono.gnome-keyring-sharp
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
cd lib
%patch8 -p1 -b .str_fmt
cd ..
%patch3 -p1 -b .multiplefile
%if %{mdkversion} >= 200900
%patch6 -p1 -b .gnome-keyring-sharp
%endif
%patch7 -p1 -b .fixunderlinking

intltoolize --force
libtoolize --copy --force
aclocal -I build/m4/shamrock -I build/m4/shave
autoconf
automake

%build
%configure2_5x \
	--disable-scrollkeeper \
	--disable-static
#parallel build is broken
make

%install
rm -rf %{buildroot} %name.lang
%makeinstall_std

rm -f %buildroot%_libdir/%name/lib*a

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

%check
make check

%clean
rm -rf %{buildroot}

%preun
%preun_uninstall_gconf_schemas %name

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS MAINTAINERS NEWS README TODO
%_sysconfdir/gconf/schemas/f-spot.schemas
%_bindir/%name
%_bindir/%name-import
%_bindir/%name-sqlite-upgrade
%dir %_libexecdir/gnome-screensaver/
%_libexecdir/gnome-screensaver/f-spot-screensaver
%dir %_libdir/%name
%_libdir/%name/*.dll*
%_libdir/%name/*.exe*
%_libdir/%name/lib*.so*
%_libdir/%name/*.addins
%dir %_libdir/%name/extensions
%_libdir/%name/extensions/CDExport.dll
%_libdir/%name/extensions/ChangePhotoPath.dll
%_libdir/%name/extensions/CoverTransition.dll
%_libdir/%name/extensions/DBusService.dll
%_libdir/%name/extensions/DevelopInUFRaw.dll
%_libdir/%name/extensions/FacebookExport.dll
%_libdir/%name/extensions/FlickrExport.dll
%_libdir/%name/extensions/FolderExport.dll
%_libdir/%name/extensions/GalleryExport.dll
%_libdir/%name/extensions/HashJob.dll
%_libdir/%name/extensions/LiveWebGallery.dll
%_libdir/%name/extensions/MergeDb.dll
%_libdir/%name/extensions/PicasaWebExport.dll
%_libdir/%name/extensions/RawPlusJpeg.dll
%_libdir/%name/extensions/RetroactiveRoll.dll
%_libdir/%name/extensions/ScreensaverConfig.dll
%_libdir/%name/extensions/SmugMugExport.dll
%_libdir/%name/extensions/TabbloExport.dll
%_libdir/%name/extensions/ZipExport.dll
%_datadir/applications/%name.desktop
%_datadir/applications/%name-import.desktop
%_datadir/applications/%name-view.desktop
%_datadir/applications/screensavers/f-spot-screensaver.desktop
%dir %_datadir/omf/*/
%_datadir/omf/*/*-C.omf
%_libdir/pkgconfig/*.pc
%_datadir/f-spot
%_iconsdir/hicolor/*/*/*
