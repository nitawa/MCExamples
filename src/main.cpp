
#include "MEDCouplingUMesh.hxx"
#include "MEDCouplingCMesh.hxx"
#include "MEDCouplingMappedExtrudedMesh.hxx"
#include "MEDCouplingFieldDouble.hxx"
#include "MEDCouplingMemArray.hxx"
#include "MEDCouplingMemArray.txx"
#include "MEDLoader.hxx"
#include <sstream>
#include <cmath>
#include <algorithm>
#include <functional>
#include <iostream>

using namespace MEDCoupling;

void printBox2D(const double* box){
  std::cout << "Bounding box:" << std::endl;
  std::cout << " (x,y) = (" << box[0] << "," << box[2] << ")" << std::endl;
  std::cout << " (X,Y) = (" << box[1] << "," << box[3] << ")" << std::endl;
}

double scalarProduct(const std::vector<double>& v1, const std::vector<double>& v2){
    double sp = 0;
    if (v1.size() != v2.size()){
        std::cerr << "dimension mismatch" << std::endl;
    }
    else{
        for (int i=0; i< v1.size(); i++){
            sp+=v1[i]*v2[i]
        }
    }

}

bool isCellConvex(const MEDCouplingUMesh* mesh, const mcIdType cellId){
    // loop over all cells, foreach cell, co
    int currentSign, previousSign;
    //mesh->getRenumArrForConsecutiveCellTypesSpec()
    mesh->computeNbOfFacesPerCell()
    const DataArrayDouble* cellCenters = mesh->computeCellCenterOfMass();
    DataArrayDouble* iCellCoordinates = mesh->getPartBarycenterAndOwner(&cellId,&cellId);
    const* double barycenterCoordinates = iCellCoordinates->getConstPointer();
    // loop over all other cells
    for (mcIdType jCell = 0; jCell < mesh->getNumberOfCells(); jCell++){
        if (cellId == jCell) continue;
        std::vector<mcIdType> jCellNodeIds;
        std::vector<double> jCellNodeCoordinates;
        mesh->getNodeIdsOfCell(jCell,jCellNodeIds);
        //for each node compute its cross product with the iCell
        for (int jCellNodeId = 0; jCellNodeId < jCellNodeIds.size(); jCellNodeId++){
            mesh->getCoordinatesOfNode(jCellNodeId, jCellNodeCoordinates);
            double crossProduct = 0;
            for (int i=0; i<jCellNodeCoordinates.size(); j++){
                crossProduct+=jCellNodeCoordinates[i]*barycenterCoordinates[i];
            } // end of loop over space dimension
            currentSign = (crossProduct < 0 ? -1 : 1);
            if (jCellNodeId > 0){
                previousSign = currentSign;
                if (previousSign * currentSign < 0) return false;
            }
        } // end of loop over cell coordinates
    } // end of loop over cells
    return true;
}
/*
    cellCenters->getTuple(iCell,coordinates);
    for (mcIdType iCell = 0; iCell < mesh->getNumberOfCells(); iCell++){
      // retrieve current cell center coordinates
      cellCenters->getTuple(iCell,coordinates);
      DataArrayDouble* iCellCoordinates = mesh->getPartBarycenterAndOwner(&iCell,&iCell);
      const* double barycenterCoordinates = iCellCoordinates->getConstPointer();
      // loop over all other cells
      for (mcIdType jCell = 0; jCell < mesh->getNumberOfCells(); jCell++){
          if (iCell == jCell) continue;
          std::vector<mcIdType> jCellNodeIds;
          std::vector<double> jCellNodeCoordinates;
          mesh->getNodeIdsOfCell(jCell,jCellNodeIds);
          //for each node compute its cross product with the iCell
          for (int jCellNodeId = 0; jCellNodeId < jCellNodeIds.size(); jCellNodeId++){
              mesh->getCoordinatesOfNode(jCellNodeId, jCellNodeCoordinates);
              double crossProduct = 0;
              for (int i=0; i<jCellNodeCoordinates.size(); j++){
                  crossProduct+=jCellNodeCoordinates[i]*barycenterCoordinates[i];
              }
              if ()
          }
      } // end f
    } // end of loop over cells
*/


void printCells(const MCAuto<DataArrayIdType> cellIdsArr){
  std::cout << "Number of cells = " << cellIdsArr->getNumberOfTuples() << std::endl;
  std::cout << "Number of elements = " << cellIdsArr->getNbOfElems() << std::endl;
}

void printBox2D(const double* box, const MCAuto<DataArrayIdType> cellIdsArr){
  printBox2D(box);
  printCells(cellIdsArr);
}

void testMesh(){
  // *--*--*--*--*--*
  // 0  1  2  3  4  5
  //   0  1  2  3  4
  const mcIdType nbOfCells=5;
  const mcIdType nbOfNodes=nbOfCells+1;
  double coords[3*nbOfNodes];
  for (int i=0;i<nbOfNodes; i++){
    coords[0+3*i]=i; // x
    coords[1+3*i]=0; // y
    coords[2+3*i]=0; // z
  }
  mcIdType *tab = new mcIdType(2*nbOfCells);
  for (int i=0; i<nbOfCells; i++){
    tab[2*i  ] = i;
    tab[2*i+1] = i+1;
  }
  //  mcIdType tab[2*nbOfCells]={0,1,1,2,2,3};
  MEDCouplingUMesh *mesh=MEDCouplingUMesh::New("M1D",1);
  mesh->allocateCells(nbOfCells);
  for (int i=0; i<nbOfCells; i++){
    mesh->insertNextCell(INTERP_KERNEL::NORM_SEG2,2,tab+2*i);
  }
  mesh->finishInsertingCells();
  mesh->getNodalConnectivity()->getNbOfElems();
  mesh->getNumberOfCells();
  DataArrayDouble *coordsArr=DataArrayDouble::New();
  coordsArr->distanceToTuple();
  coordsArr->useArray(coords,false,DeallocType::CPP_DEALLOC,nbOfNodes,3);
  mesh->setCoords(coordsArr);
  WriteUMesh("Mesh1D.med",mesh,true);
  // some checks
  // retrieve Mesh bounding box
  //  double bbox[2][2];
  double* bbox = new double(4);
  mesh->getBoundingBox( bbox ); // renvoie x,X et y,Y
  printBox2D(bbox);
  // check method getCellsInBoundingBox
  MCAuto<DataArrayIdType> cellIdsArr;
  for (int i=0;i<5; i++){
    bbox[0] = 0; bbox[1] = i;
    bbox[2] = 0; bbox[3] = i;
    cellIdsArr = mesh->getCellsInBoundingBox( bbox, 1e-7 );
    printBox2D(bbox,cellIdsArr);
  }
  // compute cell center of mass
  DataArrayDouble *centerMass = mesh->computeCellCenterOfMass();
  // now search a given point
  DataArrayDouble* point = new DataArrayDouble::New();
  double* v = new double(3);
  v[0] = 1.5; v[1] = 0.5; v[2] = 0.5;
  point->useArray(v,false, DeallocType::CPP_DEALLOC,3,1);
  centerMass->
  // bbox[0] = 0; bbox[1] = 3;
  // bbox[2] = 0; bbox[3] = 3;
  // cellIdsArr = mesh->getCellsInBoundingBox( bbox, 0.0 );
  // printBox2D(bbox,cellIdsArr);
  double* origin = new double(2);
  double* direction= new double(2);
  //mcIdType cellId;
  direction[0]=1; direction[1]=1;
  for (int i=0; i<10; i++){
    origin[0] = i*0.5;
    origin[1] = i*0.5;
    std::cout << "Origin = (x,y) = " << origin[0] << "," << origin[1] << std::endl;
    std::cout << "Trying getCellIdsCrossingPlane Algorithm" << std::endl;
    cellIdsArr = mesh->getCellIdsCrossingPlane(origin, direction, 1e-7);
    printCells(cellIdsArr);
    std::cout << "Trying getCellContainingPoint Algorithm " << std::endl;
    //mesh->getCellContainingPoint(origin, 0.1);
    std::cout << "DONE"<< std::endl;
    //std::cout << "cellId = " << cellId << std::endl;
  }
  // loop over all cells and check which one is the closest to a given point
  // retrieve all cells
  MEDCouplingUMeshCellIterator *cellIterator = mesh->cellIterator();
  cellIterator->
  cellIdsArr = mesh->getCellsInBoundingBox( mesh->getBoundingBox());
  while ( cellIdsArr->iterator()->nextt()){

  }
  for (cellIdsArr = mesh->cellIterator()->begin(); )
}

int main(int argc, char *argv[]){
  testMesh();
  std::cout << "hello" << std::endl;
  return 0;
}
