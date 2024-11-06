# -*- coding: utf-8 -*-
# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.0
# 12:25:50  10月 28, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("MONOPOLE move antenna feed and SAR")

# 定义需要设置的设计、参数值及文件路径
designs = ["HFSSDesign5", "HFSSDesign3"]
# movefeed_values = ["1mm", "2mm"]
movefeed_values = [str(value) + 'mm' for value in range(1, 11)]

file_paths = {
    "HFSSDesign5": {
        "param_file": "F:/python/phone/monopole/Antenna efficiency movefeed={}.csv",
        "field_plot_file": "F:\\python\\phone\\monopole\\monopole current move feed={}.aedtplt"
    },
    "HFSSDesign3": {
        "SAR_plot_file": "F:\\python\\phone\\monopole\\monopole SAR move feed={}.aedtplt",
        "E_plot_file": "F:\\python\\phone\\monopole\\monopole E move feed={}.aedtplt"
    }
}

# 循环遍历所有 movefeed 值
for movefeed in movefeed_values:
    for design in designs:
        oDesign = oProject.SetActiveDesign(design)
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
                            "Value:="	, movefeed
                        ]
                    ]
                ]
            ])
        oProject.Save()
        
        # 根据设计执行相应操作
        if design == "HFSSDesign5":
            oDesign.Analyze("Setup1 : Sweep")
            oModule = oDesign.GetModule("ReportSetup")
            oModule.ExportToFile("Antenna Params Plot 2", file_paths[design]["param_file"].format(movefeed), False)
            oModule = oDesign.GetModule("FieldsReporter")
            oModule.ExportFieldPlot("Vector_Jsurf1", False, file_paths[design]["field_plot_file"].format(movefeed))
        elif design == "HFSSDesign3":
            oDesign.Analyze("Setup1")
            oModule = oDesign.GetModule("FieldsReporter")
            oModule.ExportFieldPlot("Average_SAR1", False, file_paths[design]["SAR_plot_file"].format(movefeed))
            oModule.ExportFieldPlot("Vector_E1", False, file_paths[design]["E_plot_file"].format(movefeed))
