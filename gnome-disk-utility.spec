# disable to solve bootstrapping problems
%define with_nautilus 1

%if ! %{?with_nautilus}
  %define disable_nautilus --disable-nautilus
%endif

%define dbus_version              1.2
%define dbus_glib_version         0.76
%define glib2_version             2.16
%define gtk2_version              2.17.2
%define gnome_doc_utils_version   0.3.2
%define gnome_keyring_version     2.22
%define udisks_version            1.0.0
%define unique_version            1.0.4
%define libnotify_version         0.4.5
%define nautilus_version          2.26
%define libatasmart_version       0.14

Summary: Disk management application
Name: gnome-disk-utility
Version: 2.30.1
Release: 2%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://git.gnome.org/cgit/gnome-disk-utility
Source0: gnome-disk-utility-2.30.1.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: dbus-glib >= %{dbus_glib_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gnome-doc-utils >= %{gnome_doc_utils_version}
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: gnome-keyring-devel >= %{gnome_keyring_version}
BuildRequires: udisks-devel >= %{udisks_version}
BuildRequires: unique-devel >= %{unique_version}
BuildRequires: libnotify-devel >= %{libnotify_version}
%if 0%{?with_nautilus}
BuildRequires: nautilus-devel >= %{nautilus_version}
%endif
BuildRequires: libatasmart-devel >= %{libatasmart_version}
BuildRequires: avahi-ui-devel
BuildRequires: intltool
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Requires: %{name}-libs = %{version}-%{release}
Obsoletes: gnome-disk-utility-format
Obsoletes: nautilus-gdu

%description
This package contains the Palimpsest disk management application.
Palimpsest supports partitioning, file system creation, encryption,
RAID, SMART monitoring, etc.

%package libs
Summary: Shared libraries used by Palimpsest
Group: Development/Libraries
Requires: udisks >= %{udisks_version}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
This package contains libraries that are used by the Palimpsest
disk management application. The libraries in this package do not
contain UI-related code.

%package ui-libs
Summary: Shared libraries used by Palimpsest
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description ui-libs
This package contains libraries that are used by the Palimpsest
disk management application. The libraries in this package contain
disk-related widgets for use in GTK+ applications.

%package devel
Summary: Development files for gnome-disk-utility-libs
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}
Requires: pkgconfig

%description devel
This package contains header files and libraries needed to
develop applications with gnome-disk-utility-libs.

%package ui-devel
Summary: Development files for gnome-disk-utility-ui-libs
Group: Development/Libraries
Requires: %{name}-ui-libs = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: gtk2-devel >= %{gtk2_version}
Requires: pkgconfig

%description ui-devel
This package contains header files and libraries needed to
develop applications with gnome-disk-utility-ui-libs.

%prep
%setup -q

%build
%configure %{?disable_nautilus} --disable-remote-access
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# TODO: upstream doesn't ship a HACKING file yet
echo " " > HACKING

desktop-file-install --delete-original  \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/palimpsest.desktop

desktop-file-install --delete-original  \
  --dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart \
  $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/gdu-notification-daemon.desktop

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.a


%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
scrollkeeper-update
update-desktop-database %{_datadir}/applications &> /dev/null

%postun
scrollkeeper-update
update-desktop-database %{_datadir}/applications &> /dev/null

%post libs
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
/sbin/ldconfig

%postun libs
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
/sbin/ldconfig

%post ui-libs -p /sbin/ldconfig

%postun ui-libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)

%{_libexecdir}/gdu-notification-daemon
%{_sysconfdir}/xdg/autostart/gdu-notification-daemon.desktop
%if 0%{?with_nautilus}
%{_libdir}/nautilus/extensions-2.0/*.so
%endif
%{_libexecdir}/gdu-format-tool

%{_bindir}/palimpsest
%{_datadir}/applications/palimpsest.desktop

%dir %{_datadir}/gnome/help/palimpsest
%{_datadir}/gnome/help/palimpsest/*

%dir %{_datadir}/omf/palimpsest
%{_datadir}/omf/palimpsest/*

%files libs -f %{name}.lang
%defattr(-,root,root,-)

%doc README AUTHORS NEWS COPYING HACKING TODO

%{_libdir}/libgdu.so.*

# Yes, it's a bit weird to include icons in the non-UI package but the
# library returns references to these icons
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%files ui-libs
%defattr(-,root,root,-)

%{_libdir}/libgdu-gtk.so.*

%files devel
%defattr(-,root,root,-)

%{_libdir}/libgdu.so
%{_libdir}/pkgconfig/gdu.pc

%dir %{_includedir}/gnome-disk-utility
%dir %{_includedir}/gnome-disk-utility/gdu
%{_includedir}/gnome-disk-utility/gdu/*

# TODO: upstream needs to split docs for libgdu and libgdu-gtk
%dir %{_datadir}/gtk-doc/html/gnome-disk-utility
%{_datadir}/gtk-doc/html/gnome-disk-utility/*

%files ui-devel
%defattr(-,root,root,-)

%{_libdir}/libgdu-gtk.so
%{_libdir}/pkgconfig/gdu-gtk.pc

%dir %{_includedir}/gnome-disk-utility/gdu-gtk
%{_includedir}/gnome-disk-utility/gdu-gtk/*

%changelog
* Mon Mar 22 2010 David Zeuthen <davidz@redhat.com> - 2.30.1-2%{?dist}
- Rebuild
- Related: rhbz#575890

* Mon Mar 22 2010 David Zeuthen <davidz@redhat.com> - 2.30.1-1%{?dist}
- Update to 2.30.1
- Related: rhbz#575890

* Tue Feb 23 2010 David Zeuthen <davidz@redhat.com> - 2.29.90-1%{?dist}
- Update to new release for LVM2/Multipath support
- Don't include support for connecting to remote udisks instances
- Related: rhbz#548874
- Related: rhbz#548870

* Wed Jan 20 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.0-0.git20100115.4%{?dist}
- Actually apply patch for the missing include
- Resolves: #556542

* Tue Jan 19 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.0-0.git20100115.3%{?dist}
- Enable nautilus extension
- Resolves: #556552

* Mon Jan 18 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.0-0.git20100115.2%{?dist}
- Install missing include
- Resolves: #556542

* Fri Jan 15 2010 David Zeuthen <davidz@redhat.com> - 2.29.0-0.git20100115.1%{?dist}
- BR avahi-ui-devel
- Related: rhbz#543948

* Fri Jan 15 2010 David Zeuthen <davidz@redhat.com> - 2.29.0-0.git20100115%{?dist}
- Update to git snapshot with LVM support (#548870)
- Related: rhbz#543948

* Fri Dec  4 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.28.1-1.1
- Rebuild without nautilus in order to break the dependency loop

* Mon Nov  2 2009 David Zeuthen <davidz@redhat.com> - 2.28.1-1%{?dist}
- Update to 2.28.1

* Tue Oct 13 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.28.0-5%{?dist}
- Fix nautilus crashes by proper object referencing

* Mon Oct  5 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-4%{?dist}
- Incorporate fixes for translation issues from the stable upstream branch

* Fri Sep 18 2009 David Zeuthen <davidz@redhat.com> - 2.28.0-2%{?dist}
- BR libatasmart-devel

* Fri Sep 18 2009 David Zeuthen <davidz@redhat.com> - 2.28.0-1%{?dist}
- Update to upstream release 2.28.0
- Compared to previous releases, this release should whine less about SMART

* Mon Aug 17 2009 David Zeuthen <davidz@redhat.com> - 0.5-3%{?dist}
- Drop upstreamed patch

* Mon Aug 17 2009 David Zeuthen <davidz@redhat.com> - 0.5-2%{?dist}
- Rebuild

* Mon Aug 17 2009 David Zeuthen <davidz@redhat.com> - 0.5-1%{?dist}
- Update to release 0.5

* Mon Jul 27 2009 Matthias Clasen <mclasen@redhat.com> - 0.4-3%{?dist}
- Drop PolicyKit from .pc files, too

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 David Zeuthen <davidz@redhat.com> - 0.4-1%{?dist}
- Update to release 0.4

* Fri May 01 2009 David Zeuthen <davidz@redhat.com> - 0.3-1%{?dist}
- Upstream release 0.3

* Wed Apr 15 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.5.20090415git%{?dist}
- New snapshot

* Sun Apr 12 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.4.20090412git%{?dist}
- New snapshot

* Fri Apr 10 2009 Matthias Clasen <mclasen@redhat.com> - 0.3-0.3.20090406git%{?dist}
- Don't own directories that belong to hicolor-icon-theme

* Wed Apr 08 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.2.20090406git%{?dist}
- Fix bug in detecting when a PolicyKit error is returned (#494787)

* Mon Apr 06 2009 David Zeuthen <davidz@redhat.com> - 0.3-0.1.20090406git%{?dist}
- New snapshot

* Wed Mar 04 2009 David Zeuthen <davidz@redhat.com> - 0.2-2%{?dist}
- Don't crash when changing the LUKS passphrase on a device

* Mon Mar 02 2009 David Zeuthen <davidz@redhat.com> - 0.2-1%{?dist}
- Update to version 0.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.git20080720.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Matthias Clasen <mclasen@redhat.com> 0.1-0.git20080720.2%{?dist}
- Rebuild for pkgconfig provides

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> 0.1-0.git20080720.1%{?dist}
- Improve %%summary and %%description

* Fri Jul 20 2008 David Zeuthen <davidz@redhat.com> - 0.1-0.git20080720%{?dist}
- Initial Packaging
