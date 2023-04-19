/****************************************************************************
*                                                                           *
*             OpenMP MicroBenchmark Suite - Version 4.0beta                 *
*                                                                           *
*                            produced by                                    *
*                                                                           *
*             Mark Bull, Fiona Reid and Nix McDonnell                       *
*                                                                           *
*                                at                                         *
*                                                                           *
*                   EPCC, University of Edinburgh                           *
*                                                                           *
*                    email: m.bull@epcc.ed.ac.uk                            *
*                                                                           *
*                                                                           *
*      This version copyright (c) The University of Edinburgh, 2021.        *
*                                                                           *
*                                                                           *
*  Licensed under the Apache License, Version 2.0 (the "License");          *
*  you may not use this file except in compliance with the License.         *
*  You may obtain a copy of the License at                                  *
*                                                                           *
*      http://www.apache.org/licenses/LICENSE-2.0                           *
*                                                                           *
*  Unless required by applicable law or agreed to in writing, software      *
*  distributed under the License is distributed on an "AS IS" BASIS,        *
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
*  See the License for the specific language governing permissions and      *
*  limitations under the License.                                           *
*                                                                           *
****************************************************************************/


#ifndef SYNCBENCH_H
#define SYNCBENCH_H

void refer(void);

void referatom(void);

void referred(void);

void testpr(void);

void testfor(void);

void testpfor(void);

void testbar(void);

void testbarvar(void);

void testsing(void);

void testcrit(void);

void testlock(void);

void testlockhint(void);

void testlockuncontended(void);

void testlockuncontendedhint(void);

void testorder(void);

void testatom(void);

void testatomseqcst(void);

void testred(void);

#endif //SYNCBENCH_H
