#Author-Hong
#Description-test1

import adsk.core, adsk.fusion, adsk.cam, traceback, random


def makeblock(X,Y,Z):
    # 포인트를 받아오면 포인트 기준 + 방향으로 블럭 생성
    app = adsk.core.Application.get()
    ui = app.userInterface

    try:
        # Get TemporaryBRepManager
        tempBrepMgr = adsk.fusion.TemporaryBRepManager.get()

        # 중심점, 길이, 폭 방향, 길이 설정
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

        # product = app.activeProduct
        # design = adsk.fusion.Design.cast(product)
        # design.designType = adsk.fusion.DesignTypes.DirectDesignType
        #
        # # Get the root component of active design
        # rootComp = design.rootComponent
        #
        # # Get bodies in root component
        # bodies = rootComp.bRepBodies
        #
        # bodies.add(box)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    return box


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox('Hello script')

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        design.designType = adsk.fusion.DesignTypes.DirectDesignType

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create sub occurrence
        occurrences = rootComp.occurrences
        subOcc = occurrences.addNewComponent(adsk.core.Matrix3D.create())

        # Get features from sub component
        # subComponent = subOcc.component
        # features = subComponent.features

        # bRepBody를 위한 컴포넌트생성
        bodies = rootComp.bRepBodies

        for j in range(5):
            subOcc = occurrences.addNewComponent(adsk.core.Matrix3D.create())
            for i in range(10):
                bodies.add(makeblock(random.randrange(10), random.randrange(10), random.randrange(10))).moveToComponent(subOcc)

        ## 물리속성 가져오기 / 질량 중심
        # phypro = subOcc.getPhysicalProperties()
        # com = phypro.centerOfMass

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
