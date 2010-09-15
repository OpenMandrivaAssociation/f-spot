%define name 	f-spot
%define version	0.8.0
%define release	%mkrel 1

Summary:	A full-featured personal photo management application for the GNOME desktop
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch1:		f-spot-0.5.0.3-sqlite3-update.patch
Patch3: f-spot-0.6.1.3-no-multiple-files-in-viewer.patch
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
BuildRequires:  mono-flickrnet
BuildRequires:  libGConf2-devel
BuildRequires:  libgnomeui2-devel
BuildRequires:	mono-devel
BuildRequires:	mono-data-sqlite
%if %mdvver >= 201100
BuildRequires: mono-addins-devel
BuildRequires: ndesk-dbus-glib-devel
%else
BuildRequires: mono-addins
BuildRequires: ndesk-dbus-glib
%endif
BuildRequires:	libexif-devel
BuildRequires:	lcms-devel
BuildRequires:	sqlite-devel
BuildRequires:	libgphoto-devel
BuildRequires:	unique-devel
BuildRequires:	scrollkeeper
BuildRequires:	gnome-doc-utils
BuildRequires:	libxslt-proc
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
cd src/Clients/MainApp/
%patch1 -p2 -b .sqlite3-update
cd ../../../data/desktop-files/
%patch3 -p1 -b .multiplefile
cd ../..

#intltoolize --force
#libtoolize --copy --force
#aclocal -I build/m4/shamrock -I build/m4/shave -I build/m4/f-spot
#autoconf
#automake

%build
%configure2_5x \
	--disable-schemas-install \
	--disable-scrollkeeper \
	--disable-static \
	--with-gnome-screensaver-privlibexecdir=%_libdir/gnome-screensaver
#parallel build is broken
make

%install
rm -rf %{buildroot} %name.lang
%makeinstall_std

rm -f %buildroot%_libdir/%name/{lib*a,gio-sharp*,gtk-sharp-beans*}

%find_lang %name --with-gnome
#for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
#echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
#done

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
%dir %_libdir/%name/Extensions
%_libdir/%name/Extensions/FSpot.Editors.BWEditor.dll*
%_libdir/%name/Extensions/FSpot.Editors.BlackoutEditor.dll*
%_libdir/%name/Extensions/FSpot.Editors.FlipEditor.dll*
%_libdir/%name/Extensions/FSpot.Editors.PixelateEditor.dll*
%_libdir/%name/Extensions/FSpot.Editors.ResizeEditor.dll*
%_libdir/%name/Extensions/FSpot.Exporters.CD.dll*
%_libdir/%name/Extensions/FSpot.Exporters.CoverTransition.dll*
%_libdir/%name/Extensions/FSpot.Exporters.Facebook.dll*
%_libdir/%name/Extensions/FSpot.Exporters.Flickr.dll*
%_libdir/%name/Extensions/FSpot.Exporters.Folder.dll*
%_libdir/%name/Extensions/FSpot.Exporters.Gallery.dll*
%_libdir/%name/Extensions/FSpot.Exporters.PicasaWeb.dll*
%_libdir/%name/Extensions/FSpot.Exporters.SmugMug.dll*
%_libdir/%name/Extensions/FSpot.Exporters.Tabblo.dll*
%_libdir/%name/Extensions/FSpot.Exporters.Zip.dll*
%_libdir/%name/Extensions/FSpot.Tools.ChangePhotoPath.dll*
%_libdir/%name/Extensions/FSpot.Tools.DevelopInUFRaw.dll*
%_libdir/%name/Extensions/FSpot.Tools.LiveWebGallery.dll*
%_libdir/%name/Extensions/FSpot.Tools.MergeDb.dll*
%_libdir/%name/Extensions/FSpot.Tools.RawPlusJpeg.dll*
%_libdir/%name/Extensions/FSpot.Tools.RetroactiveRoll.dll*
%_libdir/%name/Extensions/FSpot.Tools.ScreensaverConfig.dll*
%_libdir/%name/Extensions/Mono.Google.dll*
%_libdir/%name/Extensions/Mono.Tabblo.dll*
%_libdir/%name/Extensions/SmugMugNet.dll*
%_datadir/applications/%name.desktop
%_datadir/applications/%name-import.desktop
%_datadir/applications/%name-view.desktop
%_datadir/applications/screensavers/f-spot-screensaver.desktop
#%dir %_datadir/omf/*/
#%_datadir/omf/*/*-C.omf
%_libdir/pkgconfig/*.pc
%_datadir/f-spot
%_iconsdir/hicolor/*/*/*
