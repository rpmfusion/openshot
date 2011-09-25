Name:           openshot
Version:        1.4.0
Release:        1%{?dist}
Summary:        A GTK based non-linear video editor 

Group:          Applications/Multimedia
# All files are GPLv3+ except for files under openshot/uploads/youtube which
# are ASL 2.0 and openshot/window/SimpleGtkBuilderApp.py which is LGPLv3 making
# the effective license of openshot GPLv3.
License:        GPLv3
URL:            http://www.openshotvideo.com/

Source0:        http://launchpad.net/openshot/1.4/%{version}/+download/openshot-%{version}.tar.gz
Patch0:         openshot-1.4.0-use_mlt-melt.diff
Patch1:         openshot-1.4.0-doc-install.diff

BuildArch: noarch

#BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: python2-devel

Requires:      mlt
Requires:      mlt-python
Requires:      notify-python
Requires:      pygoocanvas
Requires:      pygtk2-libglade
Requires:      python(abi) >= 2.5
Requires:      python-imaging
Requires:      python-httplib2
Requires:      pyxdg
Requires:      SDL
Requires:      sox
Requires:      librsvg2
Requires:      frei0r-plugins
Requires:      fontconfig


%description
OpenShot Video Editor is a free, open-source, non-linear video editor, based on
Python, GTK, and MLT. It can edit video and audio files, composite and 
transition video files, and mix multiple layers of video and audio together and 
render the output in many different formats.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Don't install unnecessary stuff
sed -i -e '/lib\/mime\/packages/d' setup.py


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT 

# Remove unnecessary .po files
rm %{buildroot}%{python_sitelib}/%{name}/locale/*/*/*.po
rm %{buildroot}%{python_sitelib}/%{name}/locale/OpenShot/OpenShot.pot
rm %{buildroot}%{python_sitelib}/%{name}/locale/README

# We strip bad shebangs (/usr/bin/env) instead of fixing them
# since these files are not executable anyways
find %{buildroot}/%{python_sitelib} -name '*.py' \
  -exec grep -q '^#!' '{}' \; -print | while read F
do
  awk '/^#!/ {if (FNR == 1) next;} {print}' $F >chopped
  touch -r $F chopped
  mv chopped $F
done

# Validate desktop file
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# modify find-lang.sh to deal with gettext .mo files under
# openshot/locale
%{__sed} -e 's|/share/locale/|/%{name}/locale/|' \
 /usr/lib/rpm/find-lang.sh \
 > find-lang-modified.sh

sh find-lang-modified.sh %{buildroot} OpenShot %{name}.lang
find %{buildroot}%{python_sitelib}/%{name}/locale -type d | while read dir
do
 echo "%%dir ${dir#%{buildroot}}" >> %{name}.lang
done


%post
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/gnome/help/openshot/
%{_datadir}/omf/openshot/
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%dir %{python_sitelib}/%{name}
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/blender
%{python_sitelib}/%{name}/classes
%{python_sitelib}/%{name}/effects
%{python_sitelib}/%{name}/export_presets
%{python_sitelib}/%{name}/images
%{python_sitelib}/%{name}/language
%{python_sitelib}/%{name}/profiles
%{python_sitelib}/%{name}/themes
%{python_sitelib}/%{name}/titles
%{python_sitelib}/%{name}/transitions
%{python_sitelib}/%{name}/uploads
%{python_sitelib}/%{name}/windows
%{python_sitelib}/*egg-info
%{_mandir}/man*/* 


%changelog
* Fri Sep 23 2011 Richard Shaw <hobbes1069@gmail.com> - 1.4.0-1
- New release.

* Tue May 31 2011 Richard Shaw <hobbes1069@gmail.com> - 1.3.1-1
- Update to latest release: 1.3.1

* Sun Apr 10 2011 Richard Shaw <hobbes1069@gmail.com> - 1.3.0-2
- Fixed spec file for packaging guidelines compliance.

* Mon Feb 14 2011 Richard Shaw <hobbes1069@gmail.com> - 1.3.0-1
- Release 1.3.0

* Thu Oct 11 2010 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.2.2-1
- Release 1.2.2

* Tue Jun 22 2010 Renich Bon Ćirić <renich@woralelandia.com> - 1.1.3-1
- Release 1.1.3

* Tue Jan 12 2010 Zarko <zarko.pintar@gmail.com> - 1.0.0-1
- Release 1.0.0

* Thu Dec 04 2009 Zarko <zarko.pintar@gmail.com> - 0.9.54-1
- initial release
