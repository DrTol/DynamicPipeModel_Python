# Dynamic Thermal Pipe Model
A dynamic heat transport model for a single pre-insulated pipe (buried underground) with thermal inertia, for district heating systems. Based on method developed by Pálsson, Hálldór (see the [Reference](README.md#Reference) below for details); A couple of partial differential equations as obtained for water-steel, insulation, and ground was solved via the implicit numerical scheme (element method).

## Table of Contents
- [How2Use](README.md#how2use)
- [License](README.md#License)
- [Acknowledgement](README.md#Acknowledgement)
- [How2Cite](README.md#How2Cite)
- [Reference](README.md#Reference)

## How2Use
Please see [ThermalPipeModel.py](https://github.com/DrTol/DynamicPipeModel_Python/blob/main/ThermalPipeModel.py) that makes use of pipe catalogue for single pre-insulated steel pipes from LOGSTOR [PipeCatalogue.py](https://github.com/DrTol/DynamicPipeModel_Python/blob/main/PipeCatalogue.py)

## License
You are free to use, modify and distribute the code as long as authorship is properly acknowledged.

## Acknowledgement
In memory of my mother Esma Tol and my father Bekir Tol.

We would like to acknowledge all of the open-source minds in general for their willing of share (as apps or comments/answers in forums), which has encouraged our department to publish our tools developed.

## How2Cite
Tol, Hİ. DynamicPipeModel_Python. DOI: 10.5281/zenodo.4182580. GitHub Repository 2020; https://github.com/DrTol/DynamicPipeModel_Python

## Reference
- Pálsson, Hálldór. Methods for planning and operating decentralized combined heat and power plants. Risø & DTU - Department of Energy Engineering (ET). Denmark. Forskningscenter Risoe. Risoe-R, No. 1185(EN) - SEE PAGES 60 - 69
