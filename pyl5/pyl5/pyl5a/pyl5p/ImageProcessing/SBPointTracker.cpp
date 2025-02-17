/*
#
#Papel y Lapiz - Software para la creacion de pequeños cortos.
#Copyright (C) 2015  Universidad de Los Andes - Proyecto DAVID.   
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation,
#Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
*/

#include "SBPointTracker.h"
#include "SBNeighborUtils.h"

SBPointTracker::SBPointTracker(void)
{
	sbShape=NULL;
}


SBPointTracker::~SBPointTracker(void)
{
}

void SBPointTracker::SetSBShape(SBShape *pSBShape) {
	sbShape=pSBShape;
}

ImageType::IndexType SBPointTracker::GetInitialB(ImageType::Pointer image) {

	ImageType::IndexType index, firstForegroundPixel;
	firstForegroundPixel[0]=-1;
	firstForegroundPixel[0]=-1;
	bool first=false;

	ConstIteratorType constIterator(image,image->GetLargestPossibleRegion());
	IteratorType iterator(image, image->GetLargestPossibleRegion());

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {
		
		if (constIterator.Value() == MAX_GRAY_VALUE) {
			if(!first) {
				firstForegroundPixel = constIterator.GetIndex();
				first=true;
			}
			else {
				index=constIterator.GetIndex();

				int neighborCount=SBNeighborUtils::GetNumberOfForegroundNeighbors(image, index);
				
				if(neighborCount==1)
					return index;
			}
			
		}
	}

	return firstForegroundPixel;
}

CBPair SBPointTracker::GetNextPathPoint(ImageType::Pointer image, ImageType::IndexType c, ImageType::IndexType b) {

	CBPair cbPair;
	ImageType::IndexType neighborIndex;
	int bX = b[0];
	int bY = b[1];
	int cX = c[0];
	int cY = c[1];

	int neighborCount = 0;

	cbPair.c = c;

	while (neighborCount < 7) {
		if (cX == bX - 1) {
			if (cY <= bY)
				cY++;
			else
				cX++;
		} else if (cX == bX) {
			if (cY == bY - 1)
				cX--;
			else
				cX++;
		} else {
			if (cY >= bY)
				cY--;
			else
				cX--;
		}

		neighborIndex[0] = cX;
		neighborIndex[1] = cY;
		ImageType::PixelType neighborValue = image->GetPixel(neighborIndex);

		if (neighborValue == MAX_GRAY_VALUE) {
			cbPair.b = neighborIndex;
			return cbPair;
		} 
		else {
			cbPair.c = neighborIndex;
		}

		neighborCount++;
	}

	neighborIndex[0] = -1;
	neighborIndex[1] = -1;

	cbPair.b = neighborIndex;
	return cbPair;
}

void SBPointTracker::TrackPoints() {

	ImageType::Pointer image=sbShape->GetImage();

	std::vector<ImageType::IndexType> points;
		
	uint numberOfForegroundPixels = SBNeighborUtils::GetTotalNumberOfForegroundPixels(image);

	ImageType::IndexType b = GetInitialB(image);
	
	if(b[0] != -1 && b[1] != -1)
	{
		points.push_back(b);

		ImageType::IndexType c;
		c[0]=b[0]-1;
		c[1]=b[1];

		ImageType::PixelType value = image->GetPixel(c);
		if (value == MAX_GRAY_VALUE)
			c[0] = b[0] + 1;

		while(points.size()!=numberOfForegroundPixels) {
			
			CBPair cbPair = GetNextPathPoint(image, c, b);
			b=cbPair.b;
			c=cbPair.c;

			sbShape->SetPoints(points);
			if(!sbShape->PointExists(b))
				points.push_back(b);
		}
		sbShape->SetPoints(points);
		
	}
	else
		std::cout << "There is no initial B" << std::endl;
}

void SBPointTracker::TrackAdvancedPoints()
{
	ImageType::Pointer image=sbShape->GetImage();

	std::vector<ImageType::IndexType> points;
		
	uint numberOfForegroundPixels = SBNeighborUtils::GetTotalNumberOfForegroundPixels(image);

	ImageType::IndexType b = GetInitialB(image);
	
	if (b[0] != -1 && b[1] != -1)
	{
		points.push_back(b);

		ImageType::IndexType c;
		c[0]=b[0]-1;
		c[1]=b[1];

		ImageType::PixelType value = image->GetPixel(c);
		if (value == MAX_GRAY_VALUE)
			c[0] = b[0] + 1;
		
		while(points.size()!=numberOfForegroundPixels)
		{
			//cout<<"SBPointTracker "<< points.size() << " "<<numberOfForegroundPixels << " " << sbShape->GetName()<<endl;
			CBPair cbPair = GetNextPathPoint(image, c, b);
			b=cbPair.b;
			c=cbPair.c;

			sbShape->SetPoints(points);
			if(!sbShape->PointExists(b))
				points.push_back(b);
		}
		
		Path path;
		path.points=points;
		vector<Path> paths;
		cout << paths.size()<<endl;
		paths.push_back(path);
		sbShape->SetPaths(paths);
	}
	else
		std::cout << "There is no initial B" << std::endl;
}

ImageType::IndexType SBPointTracker::GetIntersectionOrEndPointNeighbor(ImageType::IndexType fromIndex, ImageType::IndexType evaluatedIndex) {
	
	ImageType::IndexType neighborIndex;
	int bX = evaluatedIndex[0];
	int bY = evaluatedIndex[1];
	int cX = fromIndex[0];
	int cY = fromIndex[1];

	int neighborCount = 0;

	while (neighborCount < 7) {
		if (cX == bX - 1) {
			if (cY <= bY)
				cY++;
			else
				cX++;
		} else if (cX == bX) {
			if (cY == bY - 1)
				cX--;
			else
				cX++;
		} else {
			if (cY >= bY)
				cY--;
			else
				cX--;
		}

		neighborIndex[0] = cX;
		neighborIndex[1] = cY;

		if (sbShape->IntersectionPointExists(neighborIndex) || sbShape->EndPointExists(neighborIndex)) {
			return neighborIndex;
		}

		//std::cout<<"neighbor: "<<neighborIndex<<" value: "<< neighborValue <<std::endl;
		neighborCount++;
	}

	neighborIndex[0] = -1;
	neighborIndex[1] = -1;
	return neighborIndex;
}

void SBPointTracker::TrackEndToIntersectionOrEndToEndPaths() {
	
	bool pathFinished = false;
	ImageType::Pointer image=sbShape->GetImage();
	vector<ImageType::IndexType> endPoints=sbShape->GetEndPoints();
	vector<Path> paths=sbShape->GetPaths();

	for (uint i = 0; i < endPoints.size(); i++) {
		ImageType::IndexType b = endPoints[i];
		if (!sbShape->PointExistsInPaths(b)) {
			pathFinished = false;
			Path path;
			path.points.push_back(b);
			ImageType::IndexType c;
			c[0] = b[0] - 1;
			c[1] = b[1];
			ImageType::PixelType value = image->GetPixel(c);
			if (value == MAX_GRAY_VALUE)
				c[0] = b[0] + 1;

			while (!pathFinished) {
				CBPair cbPair = GetNextPathPoint(image, c, b);
				ImageType::IndexType newB = cbPair.b;
				ImageType::IndexType newC = cbPair.c;
				if (newB[0] != -1 && newB[1] != -1) {

					value = image->GetPixel(newB);
					ImageType::IndexType intersectionOrEndPointNeighbor = GetIntersectionOrEndPointNeighbor(path.points[path.points.size() - 1], newB);
					path.points.push_back(newB);
					if (sbShape->IntersectionPointExists(newB) || sbShape->EndPointExists(newB) || (intersectionOrEndPointNeighbor[0] != -1 && intersectionOrEndPointNeighbor[1] != -1)) {
						
						path.points.push_back(intersectionOrEndPointNeighbor);
						paths.push_back(path);
						pathFinished = true;

					} else {
						
						c = newC;
						b = newB;
					}
				}
			}
			sbShape->SetPaths(paths);
		}

	}

	
}
ImageType::IndexType SBPointTracker::GetIntersectionNeighbor(ImageType::IndexType fromIndex, ImageType::IndexType evaluatedIndex) {

	ImageType::IndexType neighborIndex;
	int bX = evaluatedIndex[0];
	int bY = evaluatedIndex[1];
	int cX = fromIndex[0];
	int cY = fromIndex[1];

	int neighborCount = 0;

	while (neighborCount < 7) {
		if (cX == bX - 1) {
			if (cY <= bY)
				cY++;
			else
				cX++;
		} else if (cX == bX) {
			if (cY == bY - 1)
				cX--;
			else
				cX++;
		} else {
			if (cY >= bY)
				cY--;
			else
				cX--;
		}

		neighborIndex[0] = cX;
		neighborIndex[1] = cY;

		if (sbShape->IntersectionPointExists(neighborIndex)) {
			return neighborIndex;
		}
		neighborCount++;
	}

	neighborIndex[0] = -1;
	neighborIndex[1] = -1;
	return neighborIndex;
}


void SBPointTracker::IterateClockwiseNeighbors(ImageType::IndexType evaluatedIndex) {

	ImageType::Pointer image=sbShape->GetImage();
	vector<Path> paths=sbShape->GetPaths();
	ImageType::IndexType neighborIndex;
	int bX = evaluatedIndex[0];
	int bY = evaluatedIndex[1];
	int cX = evaluatedIndex[0] - 1;
	int cY = evaluatedIndex[1];
	ImageType::IndexType previousNeighbor;
	previousNeighbor[0] = cX;
	previousNeighbor[1] = cY - 1;

	int neighborCount = 0;

	while (neighborCount < 8) {
		neighborIndex[0] = cX;
		neighborIndex[1] = cY;
		ImageType::PixelType neighborValue = image->GetPixel(neighborIndex);

		if (neighborValue == MAX_GRAY_VALUE) {
			if (!sbShape->IntersectionPointExists(neighborIndex)) {
				if (!sbShape->PointExistsInPaths(neighborIndex)) {
					bool pathFinished = false;
					Path path;
					path.points.push_back(evaluatedIndex);

					ImageType::IndexType b;
					ImageType::IndexType c;
					b[0] = neighborIndex[0];
					b[1] = neighborIndex[1];
					c[0] = previousNeighbor[0];
					c[1] = previousNeighbor[1];

					while (!pathFinished) {

					
						if (b[0] != -1 && b[1] != -1) {
							ImageType::IndexType intersectionNeighbor = GetIntersectionNeighbor(path.points[path.points.size()- 1], b);
							path.points.push_back(b);
							if (intersectionNeighbor[0] != -1 && intersectionNeighbor[1] != -1) {
								path.points.push_back(intersectionNeighbor);
								paths.push_back(path);
								pathFinished = true;
							} else {
								
								CBPair cbPair = GetNextPathPoint(image, c, b);
								c = cbPair.c;
								b = cbPair.b;
							}

						}

						

					}
					sbShape->SetPaths(paths);
				}
			}

		}

		previousNeighbor[0] = neighborIndex[0];
		previousNeighbor[1] = neighborIndex[1];
	
		if (cX == bX - 1) {
			if (cY <= bY)
				cY++;
			else
				cX++;
		} else if (cX == bX) {
			if (cY == bY - 1)
				cX--;
			else
				cX++;
		} else {
			if (cY >= bY)
				cY--;
			else
				cX--;
		}
		neighborCount++;
	}
}

void SBPointTracker::TrackIntersectionToIntersectionPath() {

	vector<ImageType::IndexType> intersectionPoints=sbShape->GetIntersectionPoints();
	for (uint i = 0; i < intersectionPoints.size(); i++) {
		ImageType::IndexType index = intersectionPoints[i];
		IterateClockwiseNeighbors(index);
	}
}

void SBPointTracker::TrackPaths() {
	TrackEndToIntersectionOrEndToEndPaths();
	TrackIntersectionToIntersectionPath();
}
