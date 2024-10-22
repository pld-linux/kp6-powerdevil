#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.2.2
%define		qtver		5.15.2
%define		kpname		powerdevil

Summary:	Manages the power consumption settings of a Plasma Shell
Name:		kp6-%{kpname}
Version:	6.2.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	af4c6afa099dda5dbe398cf402788779
URL:		https://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-bluez-qt-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kglobalaccel-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kidletime-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kirigami-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-knotifyconfig-devel
BuildRequires:	kf6-networkmanager-qt-devel
BuildRequires:	kf6-solid-devel
BuildRequires:	kp6-kwayland-devel
BuildRequires:	kp6-libkscreen-devel
BuildRequires:	kp6-plasma-activities-devel
BuildRequires:	kp6-plasma-workspace-devel >= %{kdeplasmaver}
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Manages the power consumption settings of a Plasma Shell.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/org_kde_powerdevil
%ghost  %{_libdir}/libpowerdevilcore.so.2
%attr(755,root,root) %{_libdir}/libpowerdevilcore.so.*.*.*
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.backlighthelper.service
%{_datadir}/polkit-1/actions/org.kde.powerdevil.backlighthelper.policy
/etc/xdg/autostart/powerdevil.desktop
%{_libdir}/libpowerdevilconfigcommonprivate.so
%{_libdir}/libpowerdevilcore.so
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.discretegpuhelper.service
%{_datadir}/polkit-1/actions/org.kde.powerdevil.discretegpuhelper.policy
%{_datadir}/dbus-1/system.d/org.kde.powerdevil.backlighthelper.conf
%{_datadir}/dbus-1/system.d/org.kde.powerdevil.discretegpuhelper.conf
%{systemduserunitdir}/plasma-powerdevil.service
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.chargethresholdhelper.service
%{_datadir}/dbus-1/system.d/org.kde.powerdevil.chargethresholdhelper.conf
%{_datadir}/polkit-1/actions/org.kde.powerdevil.chargethresholdhelper.policy

%dir %{_libdir}/qt6/plugins/powerdevil
%dir %{_libdir}/qt6/plugins/powerdevil/action
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_brightnesscontrolaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_dimdisplayaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_dpmsaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_handlebuttoneventsaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_keyboardbrightnesscontrolaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_powerprofileaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_runscriptaction.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_suspendsessionaction.so

%attr(755,root,root) %{_libdir}/libpowerdevilconfigcommonprivate.so.*.*
%ghost %{_libdir}/libpowerdevilconfigcommonprivate.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_powerdevilprofilesconfig.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/backlighthelper
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/chargethresholdhelper
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/discretegpuhelper
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/krunner/krunner_powerdevil.so
%attr(755,root,root) %{_libdir}/qt6/plugins/powerdevil/action/powerdevil_screenbrightnesscontrolaction.so
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/batterymonitor
%{_libdir}/qt6/qml/org/kde/plasma/private/batterymonitor/batterymonitorplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/batterymonitor/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/plasma/private/batterymonitor/libbatterymonitorplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/batterymonitor/qmldir
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/brightnesscontrolplugin
%{_libdir}/qt6/qml/org/kde/plasma/private/brightnesscontrolplugin/brightnesscontrolplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/brightnesscontrolplugin/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/plasma/private/brightnesscontrolplugin/libbrightnesscontrolplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/brightnesscontrolplugin/qmldir
%{_desktopdir}/kcm_powerdevilprofilesconfig.desktop
%{_datadir}/qlogging-categories6/powerdevil.categories
%{_datadir}/knotifications6/powerdevil.notifyrc
%{_datadir}/metainfo/org.kde.plasma.battery.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.brightness.appdata.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.battery
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/config
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/config/main.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui/BatteryItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui/CompactRepresentation.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui/InhibitionHint.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui/PopupDialog.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui/PowerManagementItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui/PowerProfileItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.battery/metadata.json
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.brightness
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents/ui/BrightnessItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents/ui/CompactRepresentation.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents/ui/KeyboardColorItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents/ui/NightLightItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents/ui/PopupDialog.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.brightness/metadata.json
%{_datadir}/qlogging-categories6/batterymonitor.categories
