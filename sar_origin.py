# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.0
# 18:40:54  10月 26, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("MONOPOLE move antenna feed and SAR")
oDesign = oProject.SetActiveDesign("HFSSDesign5")
oDesign.Analyze("Setup1 : Sweep")
oModule = oDesign.GetModule("ReportSetup")
oModule.ExportToFile("Antenna Params Plot 2", "F:/python/phone/monopole/Antenna efficiency movefeed=1mm.csv", False)
oModule = oDesign.GetModule("FieldsReporter")
oModule.ExportFieldPlot("Vector_Jsurf1", False, "F:\\python\\phone\\monopole\\monopole current move feed=1mm.aedtplt")
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
					"Value:="		, "2mm"
				]
			]
		]
	])
oProject.Save()
oDesign.Analyze("Setup1 : Sweep")
oModule = oDesign.GetModule("ReportSetup")
oModule.ExportToFile("Antenna Params Plot 2", "F:/python/phone/monopole/Antenna efficiency movefeed=2mm.csv", False)
oModule = oDesign.GetModule("FieldsReporter")
oModule.ExportFieldPlot("Vector_Jsurf1", False, "F:\\python\\phone\\monopole\\monopole current move feed=2mm.aedtplt")
oProject.Save()
oDesign = oProject.SetActiveDesign("HFSSDesign3")
oDesign.Analyze("Setup1")
oModule = oDesign.GetModule("FieldsReporter")
oModule.ExportFieldPlot("Average_SAR1", False, "F:\\python\\phone\\monopole\\monopole SAR move feed=2mm.aedtplt")
oModule.ExportFieldPlot("Vector_E1", False, "F:\\python\\phone\\monopole\\monopole E move feed=2mm.aedtplt")
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
					"Value:="		, "1mm"
				]
			]
		]
	])
oProject.Save()
oDesign.Analyze("Setup1")
oModule.ExportFieldPlot("Average_SAR1", False, "F:\\python\\phone\\monopole\\monopole SAR move feed=2mm.aedtplt")
oModule.ExportFieldPlot("Vector_E1", False, "F:\\python\\phone\\monopole\\monopole E move feed=2mm.aedtplt")