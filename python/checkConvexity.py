from MEDCouplingCompat import MEDCouplingUMesh
import medcoupling as mc
import MEDLoader as ml
import numpy as np
import math
def createBoxes(n,x, dx, y, dy, z, dz):
  coords = np.arange(n*3*8)
  for i in range(0,n,1):
    x = x + dx
    y = y
    z = z 
    # p0 = (x,y,z)
    coords[24*i +  0] = x
    coords[24*i +  1] = y
    coords[24*i +  2] = z
    # p1 = (x + dx, y, z)
    coords[24*i +  3] = x + dx
    coords[24*i +  4] = y
    coords[24*i +  5] = z
    # p2 = (x + dx, y + dy, z)
    coords[24*i +  6] = x + dx
    coords[24*i +  7] = y + dy
    coords[24*i +  8] = z
    # p3 = (x, y + dy, z)
    coords[24*i +  9] = x
    coords[24*i + 10] = y + dy
    coords[24*i + 11] = z
    # p4 = (x,y,z + dz)
    coords[24*i + 12] = x
    coords[24*i + 13] = y
    coords[24*i + 14] = z + dz
    # p5 = (x + dx, y, z + dz)
    coords[24*i + 15] = x + dx
    coords[24*i + 16] = y
    coords[24*i + 17] = z + dz
    # p6 = (x + dx, y + dy, z + dz)
    coords[24*i + 18] = x + dx
    coords[24*i + 19] = y + dy
    coords[24*i + 20] = z + dz
    # p7 = (x, y + dy, z + dz)
    coords[24*i + 21] = x
    coords[24*i + 22] = y + dy
    coords[24*i + 23] = z + dz
  
  # connections
  conn = []
  for i in range(0,8*n,1):
    conn.append(i)
  print(conn)
  mesh= mc.MEDCouplingUMesh.New("BOX",3)
  mesh.allocateCells(n)
  for i in range(0, n, 1):
    mesh.insertNextCell(mc.NORM_HEXA8,conn[i*8:(i+1)*8])
  mesh.finishInsertingCells()
  nodesCoords=mc.DataArrayDouble(coords.tolist(),n*8,3)
  nodesCoords.setInfoOnComponents(["X [m]","Y [m]","Z [m]"])
  mesh.setCoords(nodesCoords)
  ml.WriteUMesh("BOX.med",mesh,True) 
  return mesh

def createBox(n, x, dx, y, dy, z, dz):
  coords = np.arange(n*3*8)
  # p0 = (x,y,z)
  coords[0] = x
  coords[1] = y
  coords[2] = z
  # p1 = (x + dx, y, z)
  coords[3] = x + dx
  coords[4] = y
  coords[5] = z
  # p2 = (x + dx, y + dy, z)
  coords[6] = x + dx
  coords[7] = y + dy
  coords[8] = z
  # p3 = (x, y + dy, z)
  coords[ 9] = x
  coords[10] = y + dy
  coords[11] = z
  # p4 = (x,y,z + dz)
  coords[12] = x
  coords[13] = y
  coords[14] = z + dz
  # p5 = (x + dx, y, z + dz)
  coords[15] = x + dx
  coords[16] = y
  coords[17] = z + dz
  # p6 = (x + dx, y + dy, z + dz)
  coords[18] = x + dx
  coords[19] = y + dy
  coords[20] = z + dz
  # p7 = (x, y + dy, z + dz)
  coords[21] = x
  coords[22] = y + dy
  coords[23] = z + dz
  
  # connections
  conn = []
  conn = [ 0, 1, 2, 3, 4, 5, 6, 7] 
  print(conn, len(conn))
  mesh= mc.MEDCouplingUMesh.New("BOX",3)
  mesh.allocateCells(n)
  mesh.insertNextCell(mc.NORM_HEXA8,conn)
  mesh.finishInsertingCells()
  nodesCoords=mc.DataArrayDouble(coords.tolist(),n*8,3)
  nodesCoords.setInfoOnComponents(["X [m]","Y [m]","Z [m]"])
  mesh.setCoords(nodesCoords)
  ml.WriteUMesh("BOX.med",mesh,True) 
  return

def createMesh():
  targetCoords = [-0.3,-0.3, 0.2,-0.3, 0.7,-0.3, -0.3,0.2, 0.2,0.2, 0.7,0.2, -0.3,0.7, 0.2,0.7, 0.7,0.7 ]
  targetConn = [0,3,4,1, 1,4,2, 4,5,2, 6,7,4,3, 7,8,5,4]
  targetMesh = ml.MEDCouplingUMesh("MyMesh",2)
  targetMesh.allocateCells(5)
  targetMesh.insertNextCell(ml.NORM_TRI3,3,targetConn[4:7])
  targetMesh.insertNextCell(ml.NORM_TRI3,3,targetConn[7:10])
  targetMesh.insertNextCell(ml.NORM_QUAD4,4,targetConn[0:4])
  targetMesh.insertNextCell(ml.NORM_QUAD4,4,targetConn[10:14])
  targetMesh.insertNextCell(ml.NORM_QUAD4,4,targetConn[14:18])
  myCoords = ml.DataArrayDouble(targetCoords,9,2)
  myCoords.setInfoOnComponents(["X [km]","YY [mm]"])
  targetMesh.setCoords(myCoords)
  meshMEDFile = ml.MEDFileUMesh()
  meshMEDFile.setMeshAtLevel(0,targetMesh)
  meshMEDFile.write("TargetMeshA.med",2)
  return targetMesh

def isCellConvex(mesh, cellId, medFileName):
  numberOfFaces = mesh.computeNbOfFacesPerCell()
  nodalConnectivity = mesh.getNodalConnectivity()
  print(nodalConnectivity)
  # retrieve all node ids for current cell
  nodeIds = mesh.getNodeIdsOfCell(cellId)
  print(nodeIds)
  coordinates = []
  connexions  = []
  for nodeId in nodeIds:
    print(nodeId, mesh.getCoordinatesOfNode(nodeId))
    coordinates+= mesh.getCoordinatesOfNode(nodeId)
    connexions += [nodalConnectivity[cellId + nodeId + 1]]
    #print(coordinates)
  #return
  # reset connexion
  print("=============")
  print(connexions)
  connexions = [x - connexions[0] for x in connexions]
  print(connexions)
  print ("cell ID = ", cellId)
  print(connexions)
  # build a new mesh from these nodes
  subMesh = mc.MEDCouplingUMesh.New()
  subMesh.setName(mesh.getName())
  subMesh.setMeshDimension(mesh.getMeshDimension())
  subMesh.allocateCells(1)
  subMesh.insertNextCell(mesh.getTypeOfCell(cellId), len(nodeIds), connexions)
  subMesh.finishInsertingCells()
  print(3*len(nodeIds), "====>", len(coordinates))
  coordinates = mc.DataArrayDouble(coordinates,len(nodeIds),3)
  print("===>", coordinates)
  subMesh.setCoords(coordinates)
  ml.WriteUMesh(medFileName,subMesh,True)
  return
  # check that this cell is connexe
  # 
  submesh2D, desc, descIndx, revDesc, revDescIndx = subMesh.buildDescendingConnectivity()
  ml.WriteUMesh("BOX_subMesh.med",submesh2D,True)
  # loop over nodes 
  submesh2D = mc.MEDCouplingUMesh()
  #for cell2DId in submesh2D.getCell
  #for node in nodeIds:

  ##mesh2=mesh.buildDescendingConnectivity(desc,descIndx,revDesc,revDescIndx);
  return
  # build a new mesh with this cell only

  # loop over all nodes
  currentSign= 0
  previousSign=0
  for iNode in nodeIds:
    iNodeCoordinates = mesh.getCoordinatesOfNode(iNode)
    for jNode in nodesIds:
      if jNode == iNode:
        pass
      jNodeCoordinates = mesh.getCoordinatesOfNode(jNode)
      # compute scalar product
def createSingleMeshFromCell(medFileName, meshName, iCell):
  mesh  = mc.ReadUMeshFromFile(medFileName,meshName,0)
  for iCell in range(0, mesh.getNumberOfCells(), 1):
    cellMesh = mesh[iCell]
    outputMEDFileName = "{}_cellID_{}.med".format(meshName, iCell)
    ###cellMesh.write(outputMEDFileName)
    ml.WriteUMesh(outputMEDFileName,cellMesh,True)
  return

def checkCase():
  gMesh  = mc.ReadUMeshFromFile(r"D:\CEA\MEDCOUPLING-9.6.0\USER\MCExamples\medfiles\target.med","target",0)
  #gMesh  = mc.ReadUMeshFromFile(r"D:\CEA\MEDCOUPLING-9.6.0\USER\MCExamples\medfiles\MyMesh.med","mesh3D",0)
  gMesh  = mc.ReadUMeshFromFile(r"D:\CEA\MEDCOUPLING-9.6.0\USER\MCExamples\medfiles\oneBOX.med","BOX",0)
  for cellID in range(0, gMesh.getNumberOfCells(), 1):
    print("Checking cell : {}".format(cellID))
    cellMesh = gMesh[cellID]
    submesh2D, desc, descIndx, revDesc, revDescIndx = cellMesh.buildDescendingConnectivity()
    centerOfMass=submesh2D.computeCellCenterOfMass()
    centerOfMass = centerOfMass.getValues()
    print("Cell {} contains {} faces".format(cellID, submesh2D.getNumberOfCells()))
    iNodeNormals = submesh2D.buildOrthogonalField().getArray().getValues()
    for iCell in range(0, submesh2D.getNumberOfCells(),1):
      iNodeIds = submesh2D.getNodeIdsOfCell(iCell)
      iNodeNormal = iNodeNormals[iCell:iCell+3]
      barycenter = centerOfMass[iCell:iCell+3]
      print("face ID {}".format(iCell))
      print("  face normal: {}".format(iNodeNormal))
      print("  face barycenter {}".format(barycenter))
      print("  Number of Nodes {} ".format(len(iNodeIds),iNodeIds))
      for iNode in iNodeIds:
        iNodeCoords = submesh2D.getCoordinatesOfNode(iNode)
        print("  Inode {} coordinates {}".format(iNode,iNodeCoords))
  #return
  convexCells  = []
  concaveCells = []
  for cellID in range(0, gMesh.getNumberOfCells(), 1):
    print("Checking cell : {}".format(cellID))
    cellMesh = gMesh[cellID]
    cellMesh.orientCorrectlyPolyhedrons()
    # compute 2D mesh
    submesh2D, desc, descIndx, revDesc, revDescIndx = cellMesh.buildDescendingConnectivity()
    centerOfMass=submesh2D.computeCellCenterOfMass()
    centerOfMass = centerOfMass.getValues()
    currentSign = 0
    previousSign= 0
    firstIteration = True
    isConvex = False
    print("Cell {} contains {} faces".format(cellID, submesh2D.getNumberOfCells()))
    # build all normals at once
    iNodeNormals = submesh2D.buildOrthogonalField().getArray().getValues()
    for iCell in range(0, submesh2D.getNumberOfCells(),1):
      # compute center of mass
      iNodeIds = submesh2D.getNodeIdsOfCell(iCell)
      iNodeNormal = iNodeNormals[iCell:iCell+3]
      ###submesh2D.buildPartOrthogonalField(v).getArray().getValues()
      # compute vector from cell center of mass to that node
      barycenter = centerOfMass[iCell:iCell+3]
      print("current face ID {} normal {} barycenter: {}".format(iCell, iNodeNormal, barycenter))
      print(" Nodes {} ".format(len(iNodeIds),iNodeIds))
      for jCell in range(0, submesh2D.getNumberOfCells(),1) :
        print("Next face {}".format(jCell))
        if jCell == iCell:
          print("Face is same as one under investigation. Skipping.")
          continue
        # retrieve nodes for the current node
        jNodeIds = submesh2D.getNodeIdsOfCell(jCell)
        print("Face {} number of nodes {} list {}".format(jCell, len(jNodeIds), jNodeIds))
        for jNode in jNodeIds:
          if jNode in iNodeIds:
            print("current node {} is contained in face analysed {}".format(jNode,iCell))
            # skip current node since contained
            continue
          # retrieve coordinates for that node
          jNodeCoords = submesh2D.getCoordinatesOfNode(jNode)
          print("Current node {} coodinates {}".format(jNode, jNodeCoords))
          jVec = [i - j for i,j in zip(jNodeCoords, barycenter )]
          print("jVec {}".format(jVec))
          # compute scalar product with the normal
          dotProduct = sum([i*j for i,j in zip(iNodeNormal, jVec)])
          print("Cross product {}".format(dotProduct))
          if abs(dotProduct) < 1e-7:
            # current node is lying on plane.
            continue
          previousSign = currentSign
          currentSign = -1 if dotProduct < 0 else 1
          if firstIteration:
            previousSign = currentSign
            firstIteration = False
          else:
            if previousSign * currentSign < 0:
              print("CAUTION sign is flipping")
              isConvex = True
              break
        # end of loop over all nodes for current 2D-cell
        if isConvex:
          break
      # end of loop over all 2D-cells different from current 2D-cell
      if isConvex:
        break
    # end of loop over all 2D-cells
    if isConvex:
      convexCells.append(cellID)
    else:
      concaveCells.append(cellID)
  # summarize:
  print("Mesh {} - Number of Cells : {}".format( gMesh.getName(), gMesh.getNumberOfCells()))
  print(" - Found {} convex cells {}".format(len(convexCells),convexCells))
  print(" - Found {} concave cells {}".format(len(concaveCells),concaveCells))
  return

def main():
  #n=1; x= 1; dx = 1; y=1; dy = 1; z =1; dz = 1
  #mesh = createBoxes(n, x, dx, y, dy, z, dz)
  #return
  #medFileName = r"D:\CEA\MEDCOUPLING-9.6.0\USER\MCExamples\medfiles\target.med"
  #meshName = "target"
  #iCell = 0
  #createSingleMeshFromCell(medFileName, meshName, iCell)
  checkCase()
  return
  n=2; x= 1; dx = 1; y=2; dy = 10; z =3; dz = 5
  mesh = createBoxes(n, x, dx, y, dy, z, dz)
  submesh2D, desc, descIndx, revDesc, revDescIndx = mesh.buildDescendingConnectivity()
  ##print("MESH")
  ##print(mesh)
  print('================================')
  ##print("SUBMESH")
  ##print(submesh2D)
  ##print("desc")
  ##print(desc)
  ##print("descIndx")
  ##print(descIndx)
  ##print("revDesc")
  ##print(revDesc)
  ##print("revDescIndx")
  ##print(revDescIndx)
  #submesh2D = MEDCouplingUMesh.New()
  ##print("NODES cells")
  ##for cellID in range(0,submesh2D.getNumberOfCells(), 1):
  ##  print("cell ID",cellID)
  ##  print(submesh2D.getNodeIdsOfCell(cellID))
  ##print("normals")
  centerOfMass=submesh2D.computeCellCenterOfMass()
  centerOfMass = centerOfMass.getValues()  
  for cellID in  range(0,submesh2D.getNumberOfCells(), 1):
    # retrieve two nodes and build normal to plane
    submesh2D.getNodeIdsOfCell(cellID)
    print( submesh2D.getNodeIdsOfCell(cellID))
    #DataArrayInt([1,2,3,4],4,1)
    numberOfNodes = len(submesh2D.getNodeIdsOfCell(cellID))
    print("Number of nodes ", numberOfNodes)
    x = mc.DataArrayInt.New(submesh2D.getNodeIdsOfCell(cellID), numberOfNodes, 1)
    normals = submesh2D.buildPartOrthogonalField( x)
    print(normals.getArray())
    print("=====+++++++++")
    #normal=submesh2D.buildPartOrthogonalField( submesh2D.getNodeIdsOfCell(cellID)).getArray()
    ##print(")))))))")
    #print(normals)  
    # retrieve the node coordinates
  
  #checkCase()
  #n=5; x= 1; dx = 1; y=2; dy = 10; z =3; dz = 5
  #mesh = createBoxes(n, x, dx, y, dy, z, dz)
  #isCellConvex(mesh, 2)
  return
  targetMesh = createMesh()
  targetMeshConsti, _, _, _, _ = targetMesh.buildDescendingConnectivity()
  targetMesh1 = targetMeshConsti 
  """[[3,4,7,8]]"""
  targetMesh1.setName(targetMesh.getName())
  ###targetMesh1.write('toto.med')
  meshMEDFile = ml.MEDFileUMesh()
  #meshMEDFile.setMeshAtLevel(0,targetMesh)
  meshMEDFile.setMeshAtLevel(0,targetMesh1)
  meshMEDFile.write("TargetMeshsub.med",2)
  return

if __name__ == "__main__":
    # execute only if run as a script
    main()

