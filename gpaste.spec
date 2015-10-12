Summary:	Clipboard management system
Name:		gpaste
Version:	3.18.1.1
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://www.imagination-land.org/files/gpaste/%{name}-%{version}.tar.xz
# Source0-md5:	2aecbfadd0eac44e2e67e0e8640e1330
URL:		https://github.com/Keruspe/GPaste
BuildRequires:	clutter-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.46
BuildRequires:	gnome-control-center-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel >= 3.16
BuildRequires:	intltool
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.30
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
Suggests:	wgetpaste >= 2.26
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		alt_name	GPaste

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
Requires:	gnome-shell >= 3.14.0
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

%package -n bash-completion-%{name}
Summary:	Bash completion for GPaste commands
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
Bash completion for GPaste commands.

%package -n zsh-completion-%{name}
Summary:	zsh completion for GPaste commands
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n zsh-completion-%{name}
zsh completion for GPaste commands.

%prep
%setup -q

%build
[ -f configure ] || NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-unity \
	--enable-applet \
	--enable-vala
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la

# Install bash/zsh completion support
install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p data/completions/gpaste-client $RPM_BUILD_ROOT%{bash_compdir}
install -d $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
cp -p data/completions/_gpaste-client $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions

%find_lang %{alt_name}

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/org.gnome.GPaste.Ui.desktop
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
%attr(755,root,root) %{_bindir}/gpaste
%attr(755,root,root) %{_bindir}/gpaste-client
%{_mandir}/man1/gpaste-client.1*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/gpaste-daemon
%{_datadir}/dbus-1/services/org.gnome.GPaste.service
%{_datadir}/glib-2.0/schemas/org.gnome.GPaste.gschema.xml
%{_datadir}/gnome-control-center/keybindings/*-gpaste.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpaste.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste.so.4
%{_libdir}/girepository-1.0/GPaste-1.0.typelib

%files devel
%defattr(644,root,root,755)
%{_datadir}/gir-1.0/GPaste-1.0.gir
%{_datadir}/vala/vapi/gpaste-1.0.deps
%{_datadir}/vala/vapi/gpaste-1.0.vapi
%{_includedir}/%{name}
%{_libdir}/libgpaste.so
%{_pkgconfigdir}/gpaste-1.0.pc

%files applet
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{name}-applet
%attr(755,root,root) %{_libdir}/%{name}/%{name}-ui
%{_datadir}/appdata/org.gnome.GPaste.Applet.appdata.xml
%{_datadir}/appdata/org.gnome.GPaste.Ui.appdata.xml
%{_datadir}/dbus-1/services/org.gnome.GPaste.Applet.service
%{_datadir}/dbus-1/services/org.gnome.GPaste.Ui.service
%{_desktopdir}/org.gnome.GPaste.Applet.desktop
%{_desktopdir}/org.gnome.GPaste.Ui.desktop
/etc/xdg/autostart/org.gnome.GPaste.Applet.desktop

%files -n gnome-shell-extension-%{name}
%defattr(644,root,root,755)
%{_datadir}/gnome-shell/extensions/GPaste@gnome-shell-extensions.gnome.org
%{_datadir}/gnome-shell/search-providers/org.gnome.GPaste.search-provider.ini

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/gpaste-client

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{_datadir}/zsh/site-functions/_gpaste-client
