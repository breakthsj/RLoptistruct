#Author-Hong
#Description-test1

import adsk.core, adsk.fusion, adsk.cam, traceback, csv, random

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

# def make3Dpo(X,Y,Z):
#     # 3d ????????? ?????? / Ex.point = [{'0' : adsk.core.Point3D.create(0, 0, 0)}, {'1' : adsk.core.Point3D.create(0, 1, 0)} ...]
#     pointes = []
#     k = 0
#     for x in range(X):
#         for y in range(Y):
#             for z in range(Z):
#                 point = adsk.core.Point3D.create(x, y, z)
#                 pointes.append({'{}'.format(k): point})
#                 k += 1


def makeblock(X,Y,Z):
    # ???????????? ???????????? ????????? ?????? + ???????????? ?????? ??????
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct

    try:
        # Get TemporaryBRepManager
        tempBrepMgr = adsk.fusion.TemporaryBRepManager.get()

        # ?????????, ??????, ??? ??????, ?????? ??????
        centerPoint = adsk.core.Point3D.create(X, Y, Z);
        lengthDir = adsk.core.Vector3D.create(1.0, 0.0, 0.0)
        widthDir = adsk.core.Vector3D.create(0.0, 1.0, 0.0)
        orientedBoundingBox3D = adsk.core.OrientedBoundingBox3D.create(centerPoint,
                                                                       lengthDir,
                                                                       widthDir,
                                                                       1.0,
                                                                       1.0,
                                                                       1.0
                                                                       )

        # Create box
        box = tempBrepMgr.createBox(orientedBoundingBox3D)

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        design.designType = adsk.fusion.DesignTypes.DirectDesignType

        # Get the root component of active design
        rootComp = design.rootComponent

        # Get bodies in root component
        bodies = rootComp.bRepBodies

        bodies.add(box)
    except:
        pass


def makebox():
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct

    try:
        # ?????? ????????? ??????
        rootComp = design.rootComponent

        # ?????? ????????? ??? ??????
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane

        # ????????? ?????? ??? ?????? ???????????? ??????
        sketch = sketches.add(xyPlane)
        lines = sketch.sketchCurves.sketchLines

        # # ????????? ??????
        # point0 = adsk.core.Point3D.create(0, 0, 0)
        # point1 = adsk.core.Point3D.create(0, 1, 0)
        # point2 = adsk.core.Point3D.create(1, 1, 0)
        # point3 = adsk.core.Point3D.create(1, 0, 0)
        #
        # # ?????? ??????
        # lines_endpoint = []
        # for end_point in dict_list:
        #     lines_endpoint.append(end_point.get('end_point'))
        #
        # # ?????? ??????
        # lines.addByTwoPoints(point0, point1)
        # lines.addByTwoPoints(point1, point2)
        # lines.addByTwoPoints(point2, point3)
        # lines.addByTwoPoints(point3, point0)

        # # ????????? ?????? / Ex.point = [{'0' : adsk.core.Point3D.create(0, 0, 0)}, {'1' : adsk.core.Point3D.create(0, 1, 0)} ...]
        # pointes = []
        # k = 0
        # for i in range(3):
        #     for j in range(3):
        #         point = adsk.core.Point3D.create(i, j, 0)
        #         pointes.append({'{}'.format(k): point})
        #         k += 1
        #
        # # csv ?????? ???????????? / Ex.dict_list = [{'Line_num' : 'Line1', 'end_point' : 1}, {'Line_num' : 'Line2', 'end_point' : 2} ...]
        # csv_dir = r"C:\Users\break\Downloads\test\text.csv"
        # with open(csv_dir, 'r') as f:
        #     reader = csv.DictReader(f)
        #     dict_list = []
        #     for elemt in reader:
        #         dict_list.append(elemt)
        #
        # # ?????? ?????? / lines_endpoint = ['1', '2', ...]
        # lines_endpoint = []
        # for end_point in dict_list:
        #     lines_endpoint.append(end_point.get('end_point'))
        #     print(lines_endpoint)
        #
        # # ?????? ?????? / Ex.line.addByTwoPoint(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, 1, 0)) ...
        # last_sel_point = pointes[0].get('0')  # ????????? ??????
        #
        # for i in range(len(lines_endpoint)):
        #     for j in range(len(pointes)):
        #         if lines_endpoint[i] in pointes[j]:
        #             lines.addByTwoPoints(last_sel_point, pointes[j].get('{}'.format(j)))
        #             last_sel_point = pointes[j].get('{}'.format(j))
        #
        # lines.addByTwoPoints(last_sel_point, pointes[0].get('0'))  # ????????? ??????

        # ?????? ?????? ?????? ?????? ??? ????????????
        try:
            # # ????????? ????????????
            # profile = sketch.profiles.item(0)
            #
            # # ??????????????? ?????? ??????
            # extrudes = rootComp.features.extrudeFeatures
            # ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            #
            # # 1cm ??????
            # distance = adsk.core.ValueInput.createByReal(1)
            #
            # # ?????? ??????
            # ext_input.setDistanceExtent(False, distance)
            #
            # # ????????? ????????? ?????? ??????
            # ext_input.isSolid = True
            #
            # # ??????????????? ??????
            # extrudes.add(ext_input)

            for i in range(5):
                makeblock(random.randrange(9),random.randrange(9),random.randrange(9))


            # # ?????? ??????
            # folder = 'C:/Users/break/Downloads/test/'
            #
            # # Let the view have a chance to paint just so you can watch the progress.
            # # adsk.doEvents()
            #
            # # Construct the output filename.
            # filename = folder + 'Box'
            #
            # # Save the file as f3d.
            # exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
            # f3dOptions = exportMgr.createFusionArchiveExportOptions(filename, rootComp)
            # exportMgr.execute(f3dOptions)

        except:
            if ui:
                ui.messageBox('?????? ??????!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))