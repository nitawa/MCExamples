
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
void printCells(const MCAuto<DataArrayIdType> cellIdsArr){
  std::cout << "Number of cells = " << cellIdsArr->getNumberOfTuples() << std::endl;
  std::cout << "Number of elements = " << cellIdsArr->getNbOfElems() << std::endl;
}

void printBox2D(const double* box, const MCAuto<DataArrayIdType> cellIdsArr){
  printBox2D(box);
  printCells(cellIdsArr);
}

void testMesh(){
  // *--*--*--*
  // 0  1  2  3
  const mcIdType nbOfCells=3;
  const mcIdType nbOfNodes=4;
  double coords[3*nbOfNodes];
  for (int i=0;i<nbOfNodes; i++){
    coords[0+3*i]=i;
    coords[1+3*i]=0;
    coords[2+3*i]=0;
  }
  mcIdType *tab = new mcIdType(2*nbOfCells);
  for (int i=0; i<nbOfCells; i+=2){
    tab[i  ] = i;
    tab[i+1] = i+1;
  }
  //  mcIdType tab[2*nbOfCells]={0,1,1,2,2,3};
  MEDCouplingUMesh *mesh=MEDCouplingUMesh::New("M1D",1);
  mesh->allocateCells(nbOfCells);
  for (int i=0; i<nbOfCells; i+=2){
    mesh->insertNextCell(INTERP_KERNEL::NORM_SEG2,2,tab+i);
  }
 // mesh->insertNextCell(INTERP_KERNEL::NORM_SEG2,2,tab+2);
  //mesh->insertNextCell(INTERP_KERNEL::NORM_SEG2,2,tab+4);
  mesh->finishInsertingCells();
  mesh->getNodalConnectivity()->getNbOfElems();
  mesh->getNumberOfCells();
  DataArrayDouble *coordsArr=DataArrayDouble::New();
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
  // bbox[0] = 0; bbox[1] = 3; 
  // bbox[2] = 0; bbox[3] = 3;
  // cellIdsArr = mesh->getCellsInBoundingBox( bbox, 0.0 );
  // printBox2D(bbox,cellIdsArr);
  double* origin = new double(2);
  double* direction= new double(2);
  direction[0]=1; direction[1]=1;
  for (int i=0; i<10; i++){
    origin[0] = i*0.5;
    origin[1] = i*0.5;
    std::cout << "Origin = (x,y) = " << origin[0] << "," << origin[1] << std::endl;
    cellIdsArr = mesh->getCellIdsCrossingPlane(origin, direction, 1e-7);
    printCells(cellIdsArr);
  }
}

int main(int argc, char *argv[]){
  testMesh();
  std::cout << "hello" << std::endl;
  return 0;
}

