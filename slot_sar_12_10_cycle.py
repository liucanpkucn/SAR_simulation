# -*- coding: utf-8 -*-
# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 1:05:22  11月 01, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("slot")

# 定义需要设置的设计、参数值及文件路径
designs = ["HFSSDesign5", "HFSSDesign3"]

# Movefeed 范围 0 - 35，步长为3
movefeed_values = [str(i) + 'mm' for i in range(1, 36, 3)]

# my 范围 -73 - 72，步长为15
my_values = [str(i) + 'mm' for i in range(-73, 72, 15)]

file_paths = {
    "HFSSDesign5": {
        "param_file": "F:/python/phone/slot/SLOT EFFICIENCY my={}_movefeed={}.csv",
        "field_plot_file": "F:/python/phone/slot/LOOP CURRENT MOVE FEED={}_my={}.aedtplt"
    },
    "HFSSDesign3": {
        "SAR_plot_file": "F:/python/phone/slot/LOOP SAR MOVE FEED={}_my={}.aedtplt",
        "E_plot_file": "F:/python/phone/slot/LOOP E MOVE FEED={}_my={}.aedtplt"
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
                oModule.ExportToFile("Antenna Params Plot 2", file_paths[design]["param_file"].format(my, movefeed), False)
                oModule = oDesign.GetModule("FieldsReporter")
                oModule.ExportFieldPlot("Vector_Jsurf1", False, file_paths[design]["field_plot_file"].format(movefeed, my))
            elif design == "HFSSDesign3":
                oDesign.Analyze("Setup1")
                oModule = oDesign.GetModule("FieldsReporter")
                oModule.ExportFieldPlot("Average_SAR1", False, file_paths[design]["SAR_plot_file"].format(movefeed, my))
                oModule.ExportFieldPlot("Vector_E1", False, file_paths[design]["E_plot_file"].format(movefeed, my))

# 最后保存项目
oProject.Save()
