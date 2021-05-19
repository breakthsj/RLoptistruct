#Author-Hong
#Description-test1

import adsk.core, adsk.fusion, adsk.cam, traceback, csv

_commandId = 'MakeBoxFromCSV'
_workspaceToUse = 'FusionSolidEnvironment'
_panelToUse = 'SolidModifyPanel'

_handlers = []

def commandDefinitionById(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandDefinition id is not specified')
        return None
    commandDefinitions = ui.commandDefinitions
    commandDefinition = commandDefinitions.itemById(id)
    return commandDefinition

def commandControlByIdForPanel(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox('commandControl id is not specified')
        return None
    workspaces = ui.workspaces
    modelingWorkspace = workspaces.itemById(_workspaceToUse)
    toolbarPanels = modelingWorkspace.toolbarPanels
    toolbarPanel = toolbarPanels.itemById(_panelToUse)
    toolbarControls = toolbarPanel.controls
    toolbarControl = toolbarControls.itemById(id)
    return toolbarControl

def destroyObject(uiObj, tobeDeleteObj):
    if uiObj and tobeDeleteObj:
        if tobeDeleteObj.isValid:
            tobeDeleteObj.deleteMe()
        else:
            uiObj.messageBox('tobeDeleteObj is not a valid object')

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface


        commandName = 'MakeBox with Parameters (CSV)'
        commandDescription = 'MakeBox to a CSV (Comma Separated Values) file\n'
        commandResources = './resources/command'

        class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    makebox()
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'.format(traceback.format_exc()))

        class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    cmd = args.command
                    onExecute = CommandExecuteHandler()
                    cmd.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    _handlers.append(onExecute)

                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'.format(traceback.format_exc()))


        commandDefinitions = ui.commandDefinitions

        # check if we have the command definition
        commandDefinition = commandDefinitions.itemById(_commandId)
        if not commandDefinition:
            commandDefinition = commandDefinitions.addButtonDefinition(_commandId, commandName, commandDescription, commandResources)


        onCommandCreated = CommandCreatedHandler()
        commandDefinition.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        _handlers.append(onCommandCreated)


        workspaces = ui.workspaces
        modelingWorkspace = workspaces.itemById(_workspaceToUse)
        toolbarPanels = modelingWorkspace.toolbarPanels
        toolbarPanel = toolbarPanels.itemById(_panelToUse)
        toolbarControlsPanel = toolbarPanel.controls
        toolbarControlPanel = toolbarControlsPanel.itemById(_commandId)
        if not toolbarControlPanel:
            toolbarControlPanel = toolbarControlsPanel.addCommand(commandDefinition, '')
            toolbarControlPanel.isVisible = True
            print('The Parameter I/O command was successfully added to the create panel in modeling workspace')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        objArray = []

        commandControlPanel = commandControlByIdForPanel(_commandId)
        if commandControlPanel:
            objArray.append(commandControlPanel)

        commandDefinition = commandDefinitionById(_commandId)
        if commandDefinition:
            objArray.append(commandDefinition)

        for obj in objArray:
            destroyObject(ui, obj)

    except:
        if ui:
            ui.messageBox('AddIn Stop Failed:\n{}'.format(traceback.format_exc()))

def makebox():
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct

    try:
        # 참조 디자인 설정
        rootComp = design.rootComponent

        # 참조 스케치 면 설정
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane

        # 스케치 생성 및 라인 래퍼런스 생성
        sketch = sketches.add(xyPlane)
        lines = sketch.sketchCurves.sketchLines

        # # 포인트 생성
        # point0 = adsk.core.Point3D.create(0, 0, 0)
        # point1 = adsk.core.Point3D.create(0, 1, 0)
        # point2 = adsk.core.Point3D.create(1, 1, 0)
        # point3 = adsk.core.Point3D.create(1, 0, 0)
        #
        # # 라인 선택
        # lines_endpoint = []
        # for end_point in dict_list:
        #     lines_endpoint.append(end_point.get('end_point'))
        #
        # # 라인 생성
        # lines.addByTwoPoints(point0, point1)
        # lines.addByTwoPoints(point1, point2)
        # lines.addByTwoPoints(point2, point3)
        # lines.addByTwoPoints(point3, point0)

        # 포인트 생성 / Ex.point = [{'0' : adsk.core.Point3D.create(0, 0, 0)}, {'1' : adsk.core.Point3D.create(0, 1, 0)} ...]
        pointes = []
        k = 0
        for i in range(3):
            for j in range(3):
                point = adsk.core.Point3D.create(i, j, 0)
                pointes.append({'{}'.format(k): point})
                k += 1

        # csv 파일 받아오기 / Ex.dict_list = [{'Line_num' : 'Line1', 'end_point' : 1}, {'Line_num' : 'Line2', 'end_point' : 2} ...]
        csv_dir = r"C:\Users\break\Downloads\test\text.csv"
        with open(csv_dir, 'r') as f:
            reader = csv.DictReader(f)
            dict_list = []
            for elemt in reader:
                dict_list.append(elemt)

        # 라인 선택 / lines_endpoint = ['1', '2', ...]
        lines_endpoint = []
        for end_point in dict_list:
            lines_endpoint.append(end_point.get('end_point'))
            print(lines_endpoint)

        # 라인 생성 / Ex.line.addByTwoPoint(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, 1, 0)) ...
        last_sel_point = pointes[0].get('0')  # 시작점 고정

        for i in range(len(lines_endpoint)):
            for j in range(len(pointes)):
                if lines_endpoint[i] in pointes[j]:
                    lines.addByTwoPoints(last_sel_point, pointes[j].get('{}'.format(j)))
                    last_sel_point = pointes[j].get('{}'.format(j))

        lines.addByTwoPoints(last_sel_point, pointes[0].get('0'))  # 끝점도 고정

        # 프로 파일 생성 실패 시 예외처리
        try:
            # 사각형 프로파일
            profile = sketch.profiles.item(0)

            # 익스트루드 참조 설정
            extrudes = rootComp.features.extrudeFeatures
            ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

            # 1cm 설정
            distance = adsk.core.ValueInput.createByReal(1)

            # 방향 설정
            ext_input.setDistanceExtent(False, distance)

            # 바디가 솔리드 인지 설정
            ext_input.isSolid = True

            # 익스투르드 생성
            extrudes.add(ext_input)

            # 로컬 저장
            folder = 'C:/Users/break/Downloads/test/'

            # Let the view have a chance to paint just so you can watch the progress.
            # adsk.doEvents()

            # Construct the output filename.
            filename = folder + 'Box'

            # Save the file as f3d.
            exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
            f3dOptions = exportMgr.createFusionArchiveExportOptions(filename, rootComp)
            exportMgr.execute(f3dOptions)

        except:
            if ui:
                ui.messageBox('생성 실패!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))