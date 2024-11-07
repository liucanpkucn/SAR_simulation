# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# 12:52:02  10月 31, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("loop")
oProject.Save()
oDesign = oProject.SetActiveDesign("HFSSDesign5")
oDesign.Analyze("Setup1 : Sweep")
oModule = oDesign.GetModule("ReportSetup")
oModule.ExportToFile("Antenna Params Plot 2", "F:/python/phone/loop/LOOP EFFICIENCY MOVE FEED=2mm my=2mm.csv", False)
oModule = oDesign.GetModule("FieldsReporter")
oModule.ExportFieldPlot("Vector_Jsurf1", False, "F:\\python\\phone\\loop\\LOOP CURRENT MOVE FEED=2mm my=2mm.aedtplt")
oProject.Save()
oDesign = oProject.SetActiveDesign("HFSSDesign3")
oDesign.Analyze("Setup1")
oModule = oDesign.GetModule("FieldsReporter")
oModule.ExportFieldPlot("Average_SAR1", False, "F:\\python\\phone\\loop\\LOOP SAR MOVE FEED=2mm my=2mm.aedtplt")
oModule.ExportFieldPlot("Vector_E1", False, "F:\\python\\phone\\loop\\LOOP E MOVE FEED=2mm my=2mm.aedtplt")
oDesign = oProject.SetActiveDesign("HFSSDesign5")
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
					"Value:="		, "1mm"
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
					"Value:="		, "1mm"
				]
			]
		]
	])
oProject.Save()
oDesign.Analyze("Setup1 : Sweep")
oModule = oDesign.GetModule("ReportSetup")
oModule.ExportToFile("Antenna Params Plot 2", "F:/python/phone/loop/LOOP EFFICIENCY MOVE FEED=1mm my=1mm.csv", False)
oModule = oDesign.GetModule("FieldsReporter")
oModule.ExportFieldPlot("Vector_Jsurf1", False, "F:\\python\\phone\\loop\\LOOP CURRENT MOVE FEED=1mm my=1mm.aedtplt")
oDesign = oProject.SetActiveDesign("HFSSDesign3")
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
					"Value:="		, "1mm"
				]
			]
		]
	])
oProject.Save()
oDesign.Analyze("Setup1")
oModule = oDesign.GetModule("FieldsReporter")
oModule.ExportFieldPlot("Average_SAR1", False, "F:\\python\\phone\\loop\\LOOP SAR MOVE FEED=1mm my=1mm.aedtplt")
oModule.ExportFieldPlot("Vector_E1", False, "F:\\python\\phone\\loop\\LOOP E MOVE FEED=1mm my=1mm.aedtplt")
oProject.Save()
