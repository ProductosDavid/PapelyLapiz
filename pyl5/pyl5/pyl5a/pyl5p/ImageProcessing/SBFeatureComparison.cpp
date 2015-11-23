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
#include "SBFeatureComparison.h"
#include <iostream>
#include <math.h>

SBFeatureComparison::SBFeatureComparison(void)
{
}


SBFeatureComparison::~SBFeatureComparison(void)
{
}

void SBFeatureComparison::SetFeature1(std::vector<float> pFeature1) {
	feature1=pFeature1;
}

void SBFeatureComparison::SetFeature2(std::vector<float> pFeature2) {
	feature2=pFeature2;
}


float SBFeatureComparison::Compare() {

	if(feature1.size()!=feature2.size()) {
		std::cout << "The sizes of the 2 features are different. You must choose the same number of bins for both features." << std::endl;
		return -1;
	}

	float metric=0.0;
	for(int i=0; i<(int)feature1.size(); i++) {
		
		metric+=pow((feature1[i]-feature2[i]), 2);
	}

	return metric;
}


float SBFeatureComparison::CompareWithRotations() {
	
	float tempMetric=0.0;
	float metric=Compare();

	//A rotation of 2PI/k corresponds to a shift of +-1 element in the feature array.
	//Here we make k shifts and after each one, the altered feature is compared against the original image feature.
	//The smaller metric is the chosen one
	int count=0;
	while(count<(int)feature2.size()-1){

		float firstElement=feature2[0];
		for(int i=0; i<(int)feature2.size()-1; i++) {
			feature2[i]=feature2[i+1];
		}
		feature2[feature2.size()-1]=firstElement;

		tempMetric=Compare();

		if(tempMetric<metric) {
			metric=tempMetric;
		}

		count++;
	}

	return metric;
}
