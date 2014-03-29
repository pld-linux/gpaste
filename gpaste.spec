Summary:	Clipboard management system
Name:		gpaste
Version:	3.10
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://www.imagination-land.org/files/gpaste/%{name}-%{version}.tar.xz
# Source0-md5:	c07c89d14925508fde98eac4b069324f
URL:		https://github.com/Keruspe/GPaste
BuildRequires:	appdata-tools
BuildRequires:	clutter-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-control-center-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	intltool
BuildRequires:	pango-devel
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	systemd-units
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		alt_name	GPaste

# TODO: -lgdk missing
%define		skip_post_check_so	libgpaste-keybinder.so.3.0.0 libgpaste-applet.so.1.0.0

%description
gpasted is a clipboard management daemon with DBus interface. gpaste
is its CLI client and gpaste-settings is a tool to edit gpasted
settings.

%package libs
Summary:	Library to manage the clipboard history
Group:		Libraries

%description libs
libgpaste is a library to manage the clipboard history (used by
gpasted).

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n gnome-shell-extension-%{name}
Summary:	GNOME Shell extension for GPaste
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-shell >= 3.9.90
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n gnome-shell-extension-%{name}
%{summary}.

%package applet
Summary:	Tray icon to manage GPaste
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description applet
%{summary}.

%prep
%setup -q

%build
[ -f configure ] || NOCONFIGURE=1 ./autogen.sh
%configure \
  --disable-schemas-compile \
  --disable-silent-rules \
  --disable-unity \
  --enable-applet \
  --enable-systemd \
  --enable-vala
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la

# Install bash/zsh completion support
install -d $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions
install -pm 0644 data/completions/%{name} -t $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions
install -d $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
install -pm 0644 data/completions/_%{name} -t $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions

%find_lang %{alt_name}

# Drop useless AppData file for GPaste AppIndicator
rm $RPM_BUILD_ROOT%{_datadir}/appdata/org.gnome.GPaste.AppIndicator.appdata.xml

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/org.gnome.GPaste.Settings.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/org.gnome.GPaste.Applet.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/org.gnome.GPaste.Applet.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{alt_name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md THANKS TODO
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/gpaste-settings
%attr(755,root,root) %{_libdir}/%{name}/gpasted
%{_datadir}/appdata/org.gnome.GPaste.Settings.appdata.xml
%{_desktopdir}/org.gnome.GPaste.Settings.desktop
%{_datadir}/dbus-1/services/org.gnome.GPaste.service
%{_datadir}/glib-2.0/schemas/org.gnome.GPaste.gschema.xml
%{_datadir}/gnome-control-center/keybindings/*-gpaste.xml
%{systemduserunitdir}/gpasted.service

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpaste-applet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-applet.so.1
%attr(755,root,root) %{_libdir}/libgpaste-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-client.so.3
%attr(755,root,root) %{_libdir}/libgpaste-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-core.so.4
%attr(755,root,root) %{_libdir}/libgpaste-daemon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-daemon.so.1
%attr(755,root,root) %{_libdir}/libgpaste-gnome-shell-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-gnome-shell-client.so.0
%attr(755,root,root) %{_libdir}/libgpaste-keybinder.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-keybinder.so.3
%attr(755,root,root) %{_libdir}/libgpaste-settings-ui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-settings-ui.so.2
%attr(755,root,root) %{_libdir}/libgpaste-settings.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste-settings.so.6
%{_libdir}/girepository-1.0/GPaste-1.0.typelib

%files devel
%defattr(644,root,root,755)
%{_datadir}/gir-1.0/GPaste-1.0.gir
%{_datadir}/vala/vapi/gpaste-1.0.deps
%{_datadir}/vala/vapi/gpaste-1.0.vapi
%{_includedir}/%{name}
%{_libdir}/libgpaste-applet.so
%{_libdir}/libgpaste-client.so
%{_libdir}/libgpaste-core.so
%{_libdir}/libgpaste-daemon.so
%{_libdir}/libgpaste-gnome-shell-client.so
%{_libdir}/libgpaste-keybinder.so
%{_libdir}/libgpaste-settings-ui.so
%{_libdir}/libgpaste-settings.so
%{_pkgconfigdir}/gpaste-client-1.0.pc
%{_pkgconfigdir}/gpaste-core-1.0.pc
%{_pkgconfigdir}/gpaste-daemon-1.0.pc
%{_pkgconfigdir}/gpaste-settings-1.0.pc
%{_pkgconfigdir}/gpaste-settings-ui-1.0.pc

%files applet
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{name}-applet
%{_mandir}/man1/%{name}-applet.1.*
%{_datadir}/appdata/org.gnome.GPaste.Applet.appdata.xml
%{_desktopdir}/org.gnome.GPaste.Applet.desktop
/etc/xdg/autostart/org.gnome.GPaste.Applet.desktop

%files -n gnome-shell-extension-%{name}
%defattr(644,root,root,755)
%{_datadir}/gnome-shell/extensions/GPaste@gnome-shell-extensions.gnome.org
