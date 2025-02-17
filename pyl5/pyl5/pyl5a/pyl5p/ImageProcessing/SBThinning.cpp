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

#include "SBThinning.h"
#include "SBFilterUtils.h"
#include "SBNeighborUtils.h"
#include "SBFileUtils.h"


void SBThinning::ThinShape() {
	
	ImageType::Pointer image=sbShape->GetImage();
	image=SBFilterUtils::ThinImage(image);
	image=SBFilterUtils::RescaleImage(image, 0, MAX_GRAY_VALUE);
	sbShape->SetImage(image);
	
	SBFileUtils::WriteImage(sbShape->GetImage(), FEATURE_LOG + sbShape->GetName()+ "F5. Thinning.png");
	MakeShapeOnePixelThick();
}

void SBThinning::SetSBShape(SBShape* pSBShape)
{
	sbShape = pSBShape;
}


void SBThinning::EliminateS() {

	ImageType::Pointer image=sbShape->GetImage();
	ConstIteratorType constIterator(image, image->GetLargestPossibleRegion());
	IteratorType iterator(image, image->GetLargestPossibleRegion());

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {

		if (constIterator.Value() == MAX_GRAY_VALUE) {

			ImageType::IndexType index = constIterator.GetIndex();

			ImageType::IndexType neighborIndex;
			//top left neighbor
			neighborIndex[0] = index[0] - 1;
			neighborIndex[1] = index[1] - 1;
			ImageType::PixelType neighborValue1 = image->GetPixel(
					neighborIndex);
			//top neighbor
			neighborIndex[0] = index[0];
			neighborIndex[1] = index[1] - 1;
			ImageType::PixelType neighborValue2 = image->GetPixel(
					neighborIndex);
			//top right neighbor
			neighborIndex[0] = index[0] + 1;
			neighborIndex[1] = index[1] - 1;
			ImageType::PixelType neighborValue3 = image->GetPixel(
					neighborIndex);
			//right neighbor
			neighborIndex[0] = index[0] + 1;
			neighborIndex[1] = index[1];
			ImageType::PixelType neighborValue4 = image->GetPixel(
					neighborIndex);
			//bottom right neighbor
			neighborIndex[0] = index[0] + 1;
			neighborIndex[1] = index[1] + 1;
			ImageType::PixelType neighborValue5 = image->GetPixel(
					neighborIndex);
			//bottom neighbor
			neighborIndex[0] = index[0];
			neighborIndex[1] = index[1] + 1;
			ImageType::PixelType neighborValue6 = image->GetPixel(
					neighborIndex);
			//bottom left neighbor
			neighborIndex[0] = index[0] - 1;
			neighborIndex[1] = index[1] + 1;
			ImageType::PixelType neighborValue7 = image->GetPixel(
					neighborIndex);
			//left neighbor
			neighborIndex[0] = index[0] - 1;
			neighborIndex[1] = index[1];
			ImageType::PixelType neighborValue8 = image->GetPixel(neighborIndex);

			/*bool isS1 = neighborValue5 == MAX_GRAY_VALUE && neighborValue6 == MAX_GRAY_VALUE && neighborValue8 == MAX_GRAY_VALUE;
			bool isS2 = neighborValue4 == MAX_GRAY_VALUE && neighborValue6 == MAX_GRAY_VALUE && neighborValue7 == MAX_GRAY_VALUE;
			bool isS3 = neighborValue2 == MAX_GRAY_VALUE && neighborValue4 == MAX_GRAY_VALUE && neighborValue5 == MAX_GRAY_VALUE;
			bool isS4 = neighborValue3 == MAX_GRAY_VALUE && neighborValue4 == MAX_GRAY_VALUE && neighborValue6 == MAX_GRAY_VALUE;*/

			bool isS1 = neighborValue1 == 0 && neighborValue2 == 0
					&& neighborValue3 == 0 && neighborValue4 == 0
					&& neighborValue5 == MAX_GRAY_VALUE && neighborValue6 == MAX_GRAY_VALUE
					&& neighborValue7 == 0 && neighborValue8 == MAX_GRAY_VALUE;

			bool isS2 = neighborValue1 == 0 && neighborValue2 == 0
					&& neighborValue3 == 0 && neighborValue4 == MAX_GRAY_VALUE
					&& neighborValue5 == 0 && neighborValue6 == MAX_GRAY_VALUE
					&& neighborValue7 == MAX_GRAY_VALUE && neighborValue8 == 0;

			bool isS3 = neighborValue1 == 0 && neighborValue2 == MAX_GRAY_VALUE
					&& neighborValue3 == 0 && neighborValue4 == MAX_GRAY_VALUE
					&& neighborValue5 == MAX_GRAY_VALUE && neighborValue6 == 0
					&& neighborValue7 == 0 && neighborValue8 == 0;

			bool isS4 = neighborValue1 == 0 && neighborValue2 == 0
					&& neighborValue3 == MAX_GRAY_VALUE && neighborValue4 == MAX_GRAY_VALUE
					&& neighborValue5 == 0 && neighborValue6 == MAX_GRAY_VALUE
					&& neighborValue7 == 0 && neighborValue8 == 0;

			if(isS1 || isS2 || isS3 || isS4) {
				iterator.Set(0);
			}
		}
	}

	sbShape->SetImage(image);
}


void SBThinning::EliminateCorners() {

	ImageType::Pointer image=sbShape->GetImage();
	ConstIteratorType constIterator(image,image->GetLargestPossibleRegion());
	IteratorType iterator(image, image->GetLargestPossibleRegion());

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {

		if (constIterator.Value() == MAX_GRAY_VALUE) {

			ImageType::IndexType index = constIterator.GetIndex();

			ImageType::IndexType neighborIndex;
			//top left neighbor
			neighborIndex[0] = index[0] - 1;
			neighborIndex[1] = index[1] - 1;
			ImageType::PixelType neighborValue1 = image->GetPixel(
					neighborIndex);
			//top neighbor
			neighborIndex[0] = index[0];
			neighborIndex[1] = index[1] - 1;
			ImageType::PixelType neighborValue2 = image->GetPixel(
					neighborIndex);
			//top right neighbor
			neighborIndex[0] = index[0] + 1;
			neighborIndex[1] = index[1] - 1;
			ImageType::PixelType neighborValue3 = image->GetPixel(
					neighborIndex);
			//right neighbor
			neighborIndex[0] = index[0] + 1;
			neighborIndex[1] = index[1];
			ImageType::PixelType neighborValue4 = image->GetPixel(
					neighborIndex);
			//bottom right neighbor
			neighborIndex[0] = index[0] + 1;
			neighborIndex[1] = index[1] + 1;
			ImageType::PixelType neighborValue5 = image->GetPixel(
					neighborIndex);
			//bottom neighbor
			neighborIndex[0] = index[0];
			neighborIndex[1] = index[1] + 1;
			ImageType::PixelType neighborValue6 = image->GetPixel(
					neighborIndex);
			//bottom left neighbor
			neighborIndex[0] = index[0] - 1;
			neighborIndex[1] = index[1] + 1;
			ImageType::PixelType neighborValue7 = image->GetPixel(
					neighborIndex);
			//left neighbor
			neighborIndex[0] = index[0] - 1;
			neighborIndex[1] = index[1];
			ImageType::PixelType neighborValue8 = image->GetPixel(neighborIndex);

			bool isCorner1 = neighborValue1==0 && neighborValue2==0 && neighborValue3==0 && neighborValue4==0 && neighborValue5==0 && neighborValue6 == MAX_GRAY_VALUE && neighborValue7==0 && neighborValue8 == MAX_GRAY_VALUE;
			bool isCorner2 = neighborValue1==0 && neighborValue2==0 && neighborValue3==0 && neighborValue4 == MAX_GRAY_VALUE && neighborValue5==0 && neighborValue6 == MAX_GRAY_VALUE && neighborValue7==0 && neighborValue8==0;
			bool isCorner3 = neighborValue1==0 && neighborValue2 == MAX_GRAY_VALUE  && neighborValue3==0 && neighborValue4==0 && neighborValue5==0 && neighborValue6==0 && neighborValue7==0 && neighborValue8 == MAX_GRAY_VALUE;
			bool isCorner4 = neighborValue1==0 && neighborValue2 == MAX_GRAY_VALUE && neighborValue3==0 && neighborValue4 == MAX_GRAY_VALUE && neighborValue5==0 && neighborValue6==0 && neighborValue7==0 && neighborValue8==0;
			

			if (isCorner1 || isCorner2 || isCorner3 || isCorner4 ) {
				iterator.Set(0);
			}
		}
	}

	sbShape->SetImage(image);
}

ImageType::IndexType SBThinning::CalculateValidSeed() {
	
	ImageType::Pointer image=sbShape->GetImage();
	ConstIteratorType constIterator(image,image->GetLargestPossibleRegion());
	IteratorType iterator(image, image->GetLargestPossibleRegion());
	
	ImageType::IndexType index;
	int numberOfForegroundNeighbors=0;

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {
		
		if (constIterator.Value() == MAX_GRAY_VALUE) {
			index = constIterator.GetIndex();

			numberOfForegroundNeighbors = SBNeighborUtils::GetNumberOfForegroundNeighbors(image, index);

			if (numberOfForegroundNeighbors <= 2) {
				return index;
			}
		}
	}

	index[0] = -1;
	index[1] = -1;

	return index;
}


void SBThinning::EliminateRedundantPaths() {

	ImageType::Pointer image=sbShape->GetImage();
	ConstIteratorType constIterator(image,image->GetLargestPossibleRegion());
	IteratorType iterator(image, image->GetLargestPossibleRegion());
	
	ImageType::IndexType seed = CalculateValidSeed();

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {
		
		if (constIterator.Value() == MAX_GRAY_VALUE) {

			ImageType::IndexType index = constIterator.GetIndex();
			int numberOfForegroundNeighbors = SBNeighborUtils::GetNumberOfForegroundNeighbors(image, index);

			if (numberOfForegroundNeighbors > 2) {

				iterator.Set(0);
		
				ImageType::Pointer regionGrowingOutput = SBFilterUtils::RegionGrowing(image, seed, true, MAX_GRAY_VALUE, MAX_GRAY_VALUE, MAX_GRAY_VALUE);

				iterator.Set(MAX_GRAY_VALUE);

				ImageType::Pointer xorOutput = SBFilterUtils::Xor(image, regionGrowingOutput);
				xorOutput->SetPixel(index, 0);

				if (!SBNeighborUtils::HasForegroundPixels(xorOutput)) {
					iterator.Set(0);
				}
			}

		}
	}

	sbShape->SetImage(image);
}

void SBThinning::MakeShapeOnePixelThick() {
	EliminateS();
	EliminateCorners();
	EliminateRedundantPaths();
}
