# -*- coding: utf-8 -*-
# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 10:08:13  10月 31, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("loop antenna")

# 定义需要设置的设计、参数值及文件路径
designs = ["HFSSDesign5", "HFSSDesign3"]

# 移动馈线和 my 的值
movefeed_values = ["2mm"]
my_values = ["2mm"]

file_paths = {
    "HFSSDesign5": {
        "param_file": "F:/python/phone/dipole/DIPOLE EFFICIENCY MOVE FEED={}_my={}.csv",
        "field_plot_file": "F:/python/phone/dipole/DIPOLE CURRENT MOVE FEED={}_my={}.aedtplt"
    },
    "HFSSDesign3": {
        "SAR_plot_file": "F:/python/phone/dipole/DIPOLE SAR MOVE FEED={}_my={}.aedtplt",
        "E_plot_file": "F:/python/phone/dipole/DIPOLE E MOVE FEED={}_my={}.aedtplt"
    }
}

# 循环遍历所有 movefeed 和 my 值的组合
for movefeed in movefeed_values:
    for my in my_values:
        for design in designs:
            oDesign = oProject.SetActiveDesign(design)

            # 修改 movefeed 和 my 参数
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
                                "NAME:my",
                                "Value:=", my
                            ]
                        ]
                    ]
                ])
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
                                "Value:=", movefeed
                            ]
                        ]
                    ]
                ])
            
            oProject.Save()
            
            # 根据设计执行相应操作
            if design == "HFSSDesign5":
                oDesign.Analyze("Setup1 : Sweep")
                oModule = oDesign.GetModule("ReportSetup")
                oModule.ExportToFile("Antenna Params Plot 2", file_paths[design]["param_file"].format(movefeed, my), False)
                oModule = oDesign.GetModule("FieldsReporter")
                oModule.ExportFieldPlot("Vector_Jsurf1", False, file_paths[design]["field_plot_file"].format(movefeed, my))
            elif design == "HFSSDesign3":
                oDesign.Analyze("Setup1")
                oModule = oDesign.GetModule("FieldsReporter")
                oModule.ExportFieldPlot("Average_SAR1", False, file_paths[design]["SAR_plot_file"].format(movefeed, my))
                oModule.ExportFieldPlot("Vector_E1", False, file_paths[design]["E_plot_file"].format(movefeed, my))
