# -*- coding: utf-8 -*-
# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.0
# 18:40:54  10月 26, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

oProject = oDesktop.SetActiveProject("MONOPOLE move antenna feed and SAR")
oDesign = oProject.SetActiveDesign("HFSSDesign5")

for i in range(1, 3):
    # 设置 movefeed 参数
    movefeed_value = "{}mm".format(i)
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                [
                    "NAME:PropServers", 
                    "LocalVariables"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:movefeed",
                        "Value:=" , movefeed_value
                    ]
                ]
            ]
        ]
    )

    # 执行仿真
    oDesign.Analyze("Setup1 : Sweep")

    # 导出天线效率参数
    oModule = oDesign.GetModule("ReportSetup")
    csv_path = "F:/python/phone/monopole/Antenna efficiency movefeed={}.csv".format(movefeed_value)
    oModule.ExportToFile("Antenna Params Plot 2", csv_path, False)

    # 导出电流矢量场
    oModule = oDesign.GetModule("FieldsReporter")
    j_surf_path = "F:/python/phone/monopole/monopole current move feed={}.aedtplt".format(movefeed_value)
    oModule.ExportFieldPlot("Vector_Jsurf1", False, j_surf_path)

# 切换到另一个设计 HFSSDesign3
oDesign = oProject.SetActiveDesign("HFSSDesign3")

for i in range(1, 3):
    # 设置 movefeed 参数
    movefeed_value = "{}mm".format(i)
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                [
                    "NAME:PropServers", 
                    "LocalVariables"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:movefeed",
                        "Value:=" , movefeed_value
                    ]
                ]
            ]
        ]
    )

    # 执行仿真
    oDesign.Analyze("Setup1")

    # 导出SAR和电场矢量图
    sar_path = "F:/python/phone/monopole/monopole SAR move feed={}.aedtplt".format(movefeed_value)
    e_field_path = "F:/python/phone/monopole/monopole E move feed={}.aedtplt".format(movefeed_value)
    oModule.ExportFieldPlot("Average_SAR1", False, sar_path)
    oModule.ExportFieldPlot("Vector_E1", False, e_field_path)

oProject.Save()
