%define name 	f-spot
%define version	0.4.0
%define release	%mkrel 1

Summary: 	A full-featured personal photo management application for the GNOME desktop
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch: f-spot-0.3.2-dllmap.patch
License: 	GPL
Group: 		Graphics
Url: 		http://f-spot.org/
BuildRequires: 	gnome-sharp2 >= 2.8.0
BuildRequires: 	mono-devel
BuildRequires: 	mono-data-sqlite
BuildRequires: 	libgnomeui2-devel
BuildRequires: 	libexif-devel
BuildRequires: 	liblcms-devel
BuildRequires: 	sqlite-devel
BuildRequires: 	libgphoto-devel
BuildRequires: 	perl-XML-Parser
BuildRequires: 	desktop-file-utils
BuildRequires: 	scrollkeeper gnome-doc-utils libxslt-proc
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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

%build
%configure2_5x --disable-scrollkeeper
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std saverdir=%_libdir/gnome-screensaver/
rm -f %buildroot%_libdir/%name/libfspot*a
#menu
install -d -m 755 $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): \
	command="%{_bindir}/%{name}" \
	needs="X11" \
	section="Multimedia/Graphics" \
	icon="%name.png" \
	title="F-Spot" \
	longtitle="Image Database" \
	startup_notify="true" xdg="true"
?package(%{name}): \
	command="%{_bindir}/%{name} --view" \
	needs="KDE" \
	section=".hidden" \
	icon="%name.png" \
	title="F-Spot" \
	longtitle="Image Viewer and Database" \
	startup_notify="false" accept_url="true" multiple_files="true" \
	mimetypes="image/bmp;image/gif;image/jpeg;image/jpg;image/pjpeg;image/png;image/tiff;image/x-bmp;image/x-gray;image/x-icb;image/x-ico;image/x-png;image/x-portable-anymap;image/x-portable-bitmap;image/x-portable-graymap;image/x-portable-pixmap;image/x-psd;image/x-xbitmap;image/x-xpixmap;image/x-pcx;image/x-dcraw"  xdg="true"
?package(%{name}): \
command="%{_bindir}/%{name} --view" \
	needs="GNOME" \
	section=".hidden" \
	icon="%name.png" \
	title="F-Spot" \
	longtitle="Image Viewer and Database" \
	startup_notify="false" accept_url="true" multiple_files="true" \
	mimetypes="image/bmp;image/gif;image/jpeg;image/jpg;image/pjpeg;image/png;image/tiff;image/x-bmp;image/x-gray;image/x-icb;image/x-ico;image/x-png;image/x-portable-anymap;image/x-portable-bitmap;image/x-portable-graymap;image/x-portable-pixmap;image/x-psd;image/x-xbitmap;image/x-xpixmap;image/x-pcx;image/x-dcraw"  xdg="true"
EOF
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
%_menudir/%name
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png


