# Redirect find_lang to our patched version
%global find_lang %{_sourcedir}/openshot-find-lang.sh %{buildroot}

Name:           openshot
Version:        2.5.1
Release:        1%{?dist}
Summary:        Create and edit videos and movies

Group:          Applications/Multimedia
License:        GPLv3+
URL:            http://www.openshot.org

%global distname %{name}-qt
Source0:        https://github.com/OpenShot/%{distname}/archive/v%{version}/%{distname}-%{version}.tar.gz

# QT translation files are installed to a non-standard location
Source100:      openshot-find-lang.sh

# Add openshot-owner@rpmfusion to appdata as update_contact
Patch1:         openshot-rpmfusion-contact.patch

BuildArch:      noarch
# libopenshot is unavailable on ppc64le, see rfbz #5528
ExcludeArch:    ppc64le

# For appdata
BuildRequires:  libappstream-glib

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-qt5-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  libopenshot >= 0.2.4
BuildRequires:  libopenshot-audio >= 0.1.9
BuildRequires:  desktop-file-utils

Requires:       python%{python3_pkgversion}-httplib2
Requires:       python%{python3_pkgversion}-qt5
Requires:       python%{python3_pkgversion}-qt5-webkit
Requires:       python%{python3_pkgversion}-requests
Requires:       python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-zmq
Requires:       python%{python3_pkgversion}-libopenshot >= 0.2.4
Requires:       ffmpeg-libs >= 3.4.7

%if 0%{?fedora}
Recommends:     openshot-lang
Recommends:     font(bitstreamverasans)
Recommends:     blender >= 2.80
%else
Requires:     openshot-lang
%endif


%description
OpenShot Video Editor is a free, open-source, non-linear video editor. It
can create and edit videos and movies using many popular video, audio,
image formats.  Create videos for YouTube, Flickr, Vimeo, Metacafe, iPod,
Xbox, and many more common formats!

Features include:
* Multiple tracks (layers)
* Compositing, image overlays, and watermarks
* Audio mixing and editing
* Support for image sequences (rotoscoping)
* Key-frame animation
* Video effects (chroma-key)
* Transitions (lumas and masks)
* Titles with integrated editor and templates
* 3D animation (titles and effects)


%package lang
Summary:        Additional languages for OpenShot
Requires:       %{name} = %{version}-%{release}

%description lang
%{summary}.


%prep
%autosetup -p1 -n %{distname}-%{version}


%build
%py3_build


%install
%py3_install

# We strip bad shebangs (/usr/bin/env) instead of fixing them
# since these files are not executable anyways
find %{buildroot}/%{python3_sitelib} -name '*.py' \
  -exec grep -q '^#!' '{}' \; -print | while read F
do
  awk '/^#!/ {if (FNR == 1) next;} {print}' $F >chopped
  touch -r $F chopped
  mv chopped $F
done

# Validate desktop file
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop

%if 0%{?rhel} && 0%{?rhel} <= 7
# Move appdata file to default location
mkdir -p %{buildroot}%{_metainfodir}
mv %{buildroot}%{_datadir}/metainfo/*.appdata.xml %{buildroot}%{_metainfodir}/
%endif

# Validate appdata file
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Remove an outdated file installed into /usr/lib/mime/
rm -f %{buildroot}%{_prefix}/lib/mime/packages/openshot-qt
rmdir -p --ignore-fail-on-non-empty %{buildroot}%{_prefix}/lib/mime/packages


%find_lang OpenShot --with-qt


%if 0%{?rhel} && 0%{?rhel} <= 7
%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif


%files
%license COPYING
%doc AUTHORS README.md
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{_metainfodir}/*.appdata.xml
%{python3_sitelib}/%{name}_qt/
%exclude %{python3_sitelib}/%{name}_qt/language/*
%{python3_sitelib}/*egg-info

%files lang -f OpenShot.lang
%dir %{python3_sitelib}/%{name}_qt/language
%{python3_sitelib}/%{name}_qt/language/%{name}_lang.py
%{python3_sitelib}/%{name}_qt/language/%{name}_lang.qrc


%changelog
* Sat Mar 07 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.5.1-1
- New upstream release

* Fri Feb 14 2020 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.5.0-1
- New upstream release

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.4-5.20191002git5f08a30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.4.4-4
- Update to git HEAD for compatibility with new Blender 2.80 release
- Handle renamed metadata files

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 2.4.4-3
- Rebuild for new ffmpeg version

* Mon Apr 29 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.4.4-3
- Remove simplejson require, not actually a dependency after all
- setuptools, however, is also a runtime dependency

* Sun Apr 28 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.4.4-2
- Declare dependency on requests, simplejson Python modules

* Fri Mar 22 2019 FeRD (Frank Dana) <ferdnyc AT gmail com> - 2.4.4-1
- New upstream release

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 FeRD (Frank Dana) <ferdnyc AT gmail com> - 2.4.3-2
- Add patch to fix opening files via commandline / .desktop

* Mon Sep 3 2018 FeRD (Frank Dana) <ferdnyc AT gmail com> - 2.4.3-1
- New upstream release 2.4.3
- Update libopenshot dependency version to new 0.2.2 release
- Drop several upstreamed build fixes
- Use upstream appdata file instead of our own
- Patch upstream appdata file for missed release tag
- Add openshot-owner@rpmfusion.org as update contact in appdata
- Clean up installed files
- New translations path, update find logic and packaging

* Sat Sep 1 2018 FeRD (Frank Dana) <ferdnyc AT gmail com> - 2.4.2-2
- Updated package description
- Rebuild for updated libopenshot (with new ImageMagick)

* Tue Jul 31 2018 FeRD (Frank Dana) <ferdnyc AT gmail com> - 2.4.2-1
- New upstream release

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.1-6
- Rebuilt for Python 3.7

* Thu Mar 01 2018 Richard Shaw <hobbes1069@gmail.com> - 2.4.1-5
- Fix package ownership of locale directory, fixes RFBZ#4809.

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 17 2018 Sérgio Basto <sergio@serjux.com> - 2.4.1-3
- Add some recommends to spec
- Merge epel7 work, but we still haven't python-qt5 in epel7

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-2
- Rebuilt for ffmpeg-3.5 git

* Sat Jan 13 2018 Richard Shaw <hobbes1069@gmail.com> - 2.4.1-1
- Update to latest upstream release.

* Wed Oct 25 2017 Richard Shaw <hobbes1069@gmail.com> - 2.4.0-3
- Add recommends for Vera Sans font, fixes RFBZ#5677.

* Mon Sep 11 2017 Sérgio Basto <sergio@serjux.com> - 2.4.0-2
- Also requires libopenshot >= 0.1.8

* Fri Sep 08 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-1
- Update to 2.4.0
- Use python macros
- Remove obsolete scriptlets

* Sun Sep 03 2017 Sérgio Basto <sergio@serjux.com> - 2.3.4-1
- Update to 2.3.4

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Richard Shaw <hobbes1069@gmail.com> - 2.3.2-1
- Update to latest upstream release.

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.3.1-2
- Rebuild for ffmpeg update

* Mon Apr 03 2017 Sérgio Basto <sergio@serjux.com> - 2.3.1-1
- Update to 2.3.1

* Fri Mar 31 2017 Richard Shaw <hobbes1069@gmail.com> - 2.3.0-1
- Update to latest upstream release.

* Sat Mar 25 2017 Sérgio Basto <sergio@serjux.com> - 2.2.0-1
- Update openshot to 2.2.0

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec  4 2016 Richard Shaw <hobbes1069@gmail.com> - 2.1.0-2
- All translation files now included in openshot-lang, fixes RFBZ#4358.
- Change dependency on openshot-lang from Requires to Recommends.

* Tue Aug 30 2016 Richard Shaw <hobbes1069@gmail.com> - 2.1.0-1
- Update to latest upstream release.

* Tue Aug 23 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.7-5
- Install locale files.

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 2.0.7-4
- Rebuilt for ffmpeg-3.1.1

* Wed Jul 20 2016 Sérgio Basto <sergio@serjux.com> - 2.0.7-3
- Add python3-qt5-webkit to package requires

* Mon Apr 18 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.7-2
- Update to require python3-libopenshot.

* Fri Apr  8 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.7-1
- Update to latest upstream release.

* Fri Mar  4 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.6-1
- Update to latest upstream release.

* Mon Jan 11 2016 Richard Shaw <hobbes1069@gmail.com> - 2.0.4-1
- Update to latest upstream release.

* Mon Apr  6 2015 Richard Shaw <hobbes1069@gmail.com> - 1.4.3-3
- Fix broken icon file (BZ#3546).
- Add ladspa as a install requirement (BZ#3472).

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Oct 26 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.3-1
- Update to latest upstream release.

* Mon Feb 20 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.2-4
- Fix small packaging bug with icon.

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 06 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.2-2
- Update to latest release.
- Fixed small build problem with the buildroot path finding it's way into
  a packaged file.

* Mon Feb 06 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.2-1
- Update to latest release.

* Mon Jan 30 2012 Richard Shaw <hobbes1069@gmail.com> - 1.4.1-1
- Update to latest release.
