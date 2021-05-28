import medcoupling as mc
import MEDLoader as ml
# Build a 3D mesh from scratch mixing HEXA8 and POLYHED
coords=[0.,0.,0., 1.,1.,0., 1.,1.25,0., 1.,0.,0., 1.,1.5,0., 2.,0.,0., 2.,1.,0., 1.,2.,0., 0.,2.,0., 3.,1.,0.,
        3.,2.,0., 0.,1.,0., 1.,3.,0., 2.,2.,0., 2.,3.,0.,
        0.,0.,1., 1.,1.,1., 1.,1.25,1., 1.,0.,1., 1.,1.5,1., 2.,0.,1., 2.,1.,1., 1.,2.,1., 0.,2.,1., 3.,1.,1.,
        3.,2.,1., 0.,1.,1., 1.,3.,1., 2.,2.,1., 2.,3.,1.,
        0.,0.,2., 1.,1.,2., 1.,1.25,2., 1.,0.,2., 1.,1.5,2., 2.,0.,2., 2.,1.,2., 1.,2.,2., 0.,2.,2., 3.,1.,2.,
        3.,2.,2., 0.,1.,2., 1.,3.,2., 2.,2.,2., 2.,3.,2.,
        0.,0.,3., 1.,1.,3., 1.,1.25,3., 1.,0.,3., 1.,1.5,3., 2.,0.,3., 2.,1.,3., 1.,2.,3., 0.,2.,3., 3.,1.,3.,
        3.,2.,3., 0.,1.,3., 1.,3.,3., 2.,2.,3., 2.,3.,3.]
conn=[0,11,1,3,15,26,16,18,   1,2,4,7,13,6,-1,1,16,21,6,-1,6,21,28,13,-1,13,7,22,28,-1,7,4,19,22,-1,4,2,17,19,-1,2,1,16,17,-1,16,21,28,22,19,17,
      1,6,5,3,16,21,20,18,   13,10,9,6,28,25,24,21, 11,8,7,4,2,1,-1,11,26,16,1,-1,1,16,17,2,-1,2,17,19,4,-1,4,19,22,7,-1,7,8,23,22,-1,8,11,26,23,-1,26,16,17,19,22,23,
      7,12,14,13,22,27,29,28,  15,26,16,18,30,41,31,33, 16,17,19,22,28,21,-1,16,31,36,21,-1,21,36,43,28,-1,28,22,37,43,-1,22,19,34,37,-1,19,17,32,34,-1,17,16,31,32,-1,31,36,43,37,34,32,
      16,21,20,18,31,36,35,33,   28,25,24,21,43,40,39,36, 26,23,22,19,17,16,-1,26,41,31,16,-1,16,31,32,17,-1,17,32,34,19,-1,19,34,37,22,-1,22,23,38,37,-1,23,26,41,38,-1,41,31,32,34,37,38,
      22,27,29,28,37,42,44,43, 30,41,31,33,45,56,46,48,  31,32,34,37,43,36,-1,31,46,51,36,-1,36,51,58,43,-1,43,37,52,58,-1,37,34,49,52,-1,34,32,47,49,-1,32,31,46,47,-1,46,51,58,52,49,47,
      31,36,35,33,46,51,50,48,  43,40,39,36,58,55,54,51, 41,38,37,34,32,31,-1,41,56,46,31,-1,31,46,47,32,-1,32,47,49,34,-1,34,49,52,37,-1,37,38,53,52,-1,38,41,56,53,-1,56,46,47,49,52,53,
      37,42,44,43,52,57,59,58]
mesh3D = mc.MEDCouplingUMesh("mesh3D",3);
mesh3D.allocateCells(18);
mesh3D.insertNextCell(mc.NORM_HEXA8,conn[0:8]); mesh3D.insertNextCell(mc.NORM_POLYHED,conn[8:51]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[51:59]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[59:67]); mesh3D.insertNextCell(mc.NORM_POLYHED,conn[67:110]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[110:118]);
mesh3D.insertNextCell(mc.NORM_HEXA8,conn[118:126]); mesh3D.insertNextCell(mc.NORM_POLYHED,conn[126:169]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[169:177]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[177:185]); mesh3D.insertNextCell(mc.NORM_POLYHED,conn[185:228]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[228:236]);
mesh3D.insertNextCell(mc.NORM_HEXA8,conn[236:244]); mesh3D.insertNextCell(mc.NORM_POLYHED,conn[244:287]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[287:295]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[295:303]); mesh3D.insertNextCell(mc.NORM_POLYHED,conn[303:346]); mesh3D.insertNextCell(mc.NORM_HEXA8,conn[346:354]);
myCoords = mc.DataArrayDouble(coords,60,3);
myCoords.setInfoOnComponents(["X [m]","Y [m]","Z [m]"])
mesh3D.setCoords(myCoords);
mesh3D.orientCorrectlyPolyhedrons()
mesh3D.sortCellsInMEDFileFrmt()
ml.WriteUMesh("MyMesh.med",mesh3D,True)
