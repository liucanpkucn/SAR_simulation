import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")

# 初始化并打开项目和设计
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("monopole")
oDesign = oProject.SetActiveDesign("HFSSDesign5")
oEditor = oDesign.SetActiveEditor("3D Modeler")

# 定义变量my，初始值为1mm
def define_variable(variable_name, value):
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                [
                    "NAME:PropServers", "LocalVariables"
                ],
                [
                    "NAME:NewProps",
                    [
                        "NAME:" + variable_name,
                        "PropType:=", "VariableProp",
                        "UserDef:=", True,
                        "Value:=", f"{value}mm"
                    ]
                ]
            ]
        ]
    )

define_variable("my", 1)

# 设置对象移动
def move_objects(objects, vector_x, vector_y, vector_z):
    oEditor.Move(
        [
            "NAME:Selections",
            "Selections:=", ",".join(objects),
            "NewPartsModelFlag:=", "Model"
        ],
        [
            "NAME:TranslateParameters",
            "TranslateVectorX:=", vector_x,
            "TranslateVectorY:=", vector_y,
            "TranslateVectorZ:=", vector_z
        ]
    )

# 初次移动对象Rectangle2和Rectangle3
move_objects(["Rectangle2", "Rectangle3"], "0mm", "1mm", "0mm")

# 设置参数化扫描
def insert_parametric_setup(variable, start, stop, step):
    oModule = oDesign.GetModule("Optimetrics")
    oModule.InsertSetup("OptiParametric",
        [
            "NAME:ParametricSetup1",
            "IsEnabled:=", True,
            [
                "NAME:ProdOptiSetupDataV2",
                "SaveFields:=", True,
                "CopyMesh:=", False,
                "SolveWithCopiedMeshOnly:=", True
            ],
            [
                "NAME:StartingPoint"
            ],
            "Sim. Setups:=", ["Setup1"],
            [
                "NAME:Sweeps",
                [
                    "NAME:SweepDefinition",
                    "Variable:=", variable,
                    "Data:=", f"LIN {start}mm {stop}mm {step}mm",
                    "OffsetF1:=", False,
                    "Synchronize:=", 0
                ]
            ],
            [
                "NAME:Sweep Operations"
            ],
            [
                "NAME:Goals"
            ]
        ])
    oProject.Save()
    oModule.SolveSetup("ParametricSetup1")

# 插入参数化扫描，my从0.5mm到1.5mm，步长为0.5mm
insert_parametric_setup("my", 0.5, 1.5, 0.5)

# 导出电流场数据的函数
def export_field_plot(variable_name, values, file_prefix, file_path):
    oModule = oDesign.GetModule("FieldsReporter")
    for value in values:
        # 更新变量值
        oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers", "LocalVariables"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:" + variable_name,
                            "Value:=", f"{value}mm"
                        ]
                    ]
                ]
            ]
        )
        # 导出场图
        file_name = f"{file_path}\\{file_prefix}{value}.aedtplt"
        oModule.ExportFieldPlot("Vector_Jsurf1", False, file_name)

# 设置导出路径并导出电流场数据
export_path = "F:\\python\\phone\\phone2"
export_field_plot("my", [0.5, 1, 1.5], "move", export_path)
