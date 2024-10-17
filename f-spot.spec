#gw workaround for urpmi bug 29356
#define _provides_exceptions mono.libgphoto2-sharp\\|mono.gnome-keyring-sharp\\|mono.gtk-sharp-beans\\|mono.gio-sharp

Summary:	A full-featured personal photo management application for the GNOME desktop
Name:		f-spot
Version:	0.8.2
Release:	4.2
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch0:		f-spot-fix-linking.patch
Patch3: 	f-spot-0.6.1.3-no-multiple-files-in-viewer.patch
#https://bugzilla.gnome.org/show_bug.cgi?id=629224
Patch5: 	f-spot-mono2.8.patch
License:	GPLv2+
Group: 		Graphics
Url:		https://f-spot.org
BuildRequires:	intltool
BuildRequires:	pkgconfig(gnome-sharp-2.0)
BuildRequires:	pkgconfig(gnome-desktop-sharp-2.0)
BuildRequires:  gnome-keyring-sharp
BuildRequires:  mono-flickrnet
BuildRequires:  pkgconfig(libgnomeui-2.0)
BuildRequires:	mono-devel
BuildRequires:	mono-addins-devel
BuildRequires:	ndesk-dbus-glib-devel
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	scrollkeeper
BuildRequires:	gnome-doc-utils
BuildRequires:	libxslt-proc
BuildRequires:  gnome-screensaver
BuildRequires:  gettext-devel
#gw required for the upgrade script
Requires:	sqlite-tools
Requires:	sqlite3-tools
Requires(post): shared-mime-info scrollkeeper
Requires(postun): shared-mime-info scrollkeeper

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
%patch0 -p1
cd data/desktop-files/
%patch3 -p1 -b .multiplefile
cd ../..
%patch5 -p1
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
make LIBS="-lm"

%install
%makeinstall_std

rm -f %buildroot%_libdir/%name/lib*a
#,gio-sharp*,gtk-sharp-beans*}

%find_lang %{name} --with-gnome

%check
make check

%preun
%preun_uninstall_gconf_schemas %name

%files -f %name.lang
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
%_libdir/pkgconfig/*.pc
%_datadir/f-spot
%_iconsdir/hicolor/*/*/*
