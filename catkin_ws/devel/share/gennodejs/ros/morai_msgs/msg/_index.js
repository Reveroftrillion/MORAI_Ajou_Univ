
"use strict";

let ExternalForce = require('./ExternalForce.js');
let MoraiSimProcStatus = require('./MoraiSimProcStatus.js');
let RPY = require('./RPY.js');
let SkidSteer6wUGVStatus = require('./SkidSteer6wUGVStatus.js');
let AttachmentDeviceState = require('./AttachmentDeviceState.js');
let VehicleCollisionData = require('./VehicleCollisionData.js');
let SVADC = require('./SVADC.js');
let WaitForTickResponse = require('./WaitForTickResponse.js');
let MoraiTLInfo = require('./MoraiTLInfo.js');
let EgoDdVehicleStatus = require('./EgoDdVehicleStatus.js');
let CtrlCmd = require('./CtrlCmd.js');
let MultiPlayEventRequest = require('./MultiPlayEventRequest.js');
let RadarDetection = require('./RadarDetection.js');
let EventInfo = require('./EventInfo.js');
let SyncModeCtrlCmd = require('./SyncModeCtrlCmd.js');
let EgoVehicleStatusExtended = require('./EgoVehicleStatusExtended.js');
let SyncModeCmdResponse = require('./SyncModeCmdResponse.js');
let FaultStatusInfo_Sensor = require('./FaultStatusInfo_Sensor.js');
let FaultStatusInfo = require('./FaultStatusInfo.js');
let WheelControl = require('./WheelControl.js');
let FaultStatusInfo_Vehicle = require('./FaultStatusInfo_Vehicle.js');
let Conveyor = require('./Conveyor.js');
let MoraiTLIndex = require('./MoraiTLIndex.js');
let SyncModeSetGear = require('./SyncModeSetGear.js');
let FaultStatusInfo_Overall = require('./FaultStatusInfo_Overall.js');
let UGVServeSkidCtrlCmd = require('./UGVServeSkidCtrlCmd.js');
let FaultInjection_Response = require('./FaultInjection_Response.js');
let EgoNoisyStatus = require('./EgoNoisyStatus.js');
let GripperState = require('./GripperState.js');
let FaultInjection_Controller = require('./FaultInjection_Controller.js');
let SetTrafficLight = require('./SetTrafficLight.js');
let SyncModeAddObject = require('./SyncModeAddObject.js');
let EgoDetailStatus = require('./EgoDetailStatus.js');
let SyncModeScenarioLoad = require('./SyncModeScenarioLoad.js');
let SaveSensorData = require('./SaveSensorData.js');
let VehicleSpec = require('./VehicleSpec.js');
let IntersectionStatus = require('./IntersectionStatus.js');
let RadarDetections = require('./RadarDetections.js');
let VelocityCmd = require('./VelocityCmd.js');
let SensorPosControl = require('./SensorPosControl.js');
let IntscnTL = require('./IntscnTL.js');
let SyncModeRemoveObject = require('./SyncModeRemoveObject.js');
let ShipState = require('./ShipState.js');
let ObjectStatusExtended = require('./ObjectStatusExtended.js');
let ObjectStatusList = require('./ObjectStatusList.js');
let GVStateCmd = require('./GVStateCmd.js');
let TOF = require('./TOF.js');
let SyncModeCmd = require('./SyncModeCmd.js');
let WaitForTick = require('./WaitForTick.js');
let GVDirectCmd = require('./GVDirectCmd.js');
let XYZ = require('./XYZ.js');
let GhostMessage = require('./GhostMessage.js');
let SkateboardCtrlCmd = require('./SkateboardCtrlCmd.js');
let ScenarioLoad = require('./ScenarioLoad.js');
let DillyCmdResponse = require('./DillyCmdResponse.js');
let ObjectStatusListExtended = require('./ObjectStatusListExtended.js');
let PRCtrlCmd = require('./PRCtrlCmd.js');
let ReplayInfo = require('./ReplayInfo.js');
let MultiEgoSetting = require('./MultiEgoSetting.js');
let Lamps = require('./Lamps.js');
let VehicleSpecIndex = require('./VehicleSpecIndex.js');
let MultiPlayEventResponse = require('./MultiPlayEventResponse.js');
let SkateboardStatus = require('./SkateboardStatus.js');
let PREvent = require('./PREvent.js');
let MoraiSrvResponse = require('./MoraiSrvResponse.js');
let MSITCustomMessage = require('./MSITCustomMessage.js');
let ObjectStatus = require('./ObjectStatus.js');
let GetTrafficLightStatus = require('./GetTrafficLightStatus.js');
let IntersectionControl = require('./IntersectionControl.js');
let RobotOutput = require('./RobotOutput.js');
let TrafficLight = require('./TrafficLight.js');
let SyncModeInfo = require('./SyncModeInfo.js');
let Obstacle = require('./Obstacle.js');
let ManipulatorControl = require('./ManipulatorControl.js');
let SkidSteer6wUGVCtrlCmd = require('./SkidSteer6wUGVCtrlCmd.js');
let FaultInjection_Tire = require('./FaultInjection_Tire.js');
let WoowaDillyStatus = require('./WoowaDillyStatus.js');
let FaultInjection_Sensor = require('./FaultInjection_Sensor.js');
let MoraiSimProcHandle = require('./MoraiSimProcHandle.js');
let MapSpec = require('./MapSpec.js');
let CMDConveyor = require('./CMDConveyor.js');
let RobotPose = require('./RobotPose.js');
let GPSMessage = require('./GPSMessage.js');
let ENU = require('./ENU.js');
let NpcGhostCmd = require('./NpcGhostCmd.js');
let ERP42Info = require('./ERP42Info.js');
let CollisionData = require('./CollisionData.js');
let EgoVehicleStatus = require('./EgoVehicleStatus.js');
let DdCtrlCmd = require('./DdCtrlCmd.js');
let Transforms = require('./Transforms.js');
let ShipCtrlCmd = require('./ShipCtrlCmd.js');
let SyncModeResultResponse = require('./SyncModeResultResponse.js');
let Competition = require('./Competition.js');
let RobotState = require('./RobotState.js');
let VehicleCollision = require('./VehicleCollision.js');
let MapSpecIndex = require('./MapSpecIndex.js');
let Obstacles = require('./Obstacles.js');
let DillyCmd = require('./DillyCmd.js');
let PRStatus = require('./PRStatus.js');
let GeoVector3Message = require('./GeoVector3Message.js');
let NpcGhostInfo = require('./NpcGhostInfo.js');

module.exports = {
  ExternalForce: ExternalForce,
  MoraiSimProcStatus: MoraiSimProcStatus,
  RPY: RPY,
  SkidSteer6wUGVStatus: SkidSteer6wUGVStatus,
  AttachmentDeviceState: AttachmentDeviceState,
  VehicleCollisionData: VehicleCollisionData,
  SVADC: SVADC,
  WaitForTickResponse: WaitForTickResponse,
  MoraiTLInfo: MoraiTLInfo,
  EgoDdVehicleStatus: EgoDdVehicleStatus,
  CtrlCmd: CtrlCmd,
  MultiPlayEventRequest: MultiPlayEventRequest,
  RadarDetection: RadarDetection,
  EventInfo: EventInfo,
  SyncModeCtrlCmd: SyncModeCtrlCmd,
  EgoVehicleStatusExtended: EgoVehicleStatusExtended,
  SyncModeCmdResponse: SyncModeCmdResponse,
  FaultStatusInfo_Sensor: FaultStatusInfo_Sensor,
  FaultStatusInfo: FaultStatusInfo,
  WheelControl: WheelControl,
  FaultStatusInfo_Vehicle: FaultStatusInfo_Vehicle,
  Conveyor: Conveyor,
  MoraiTLIndex: MoraiTLIndex,
  SyncModeSetGear: SyncModeSetGear,
  FaultStatusInfo_Overall: FaultStatusInfo_Overall,
  UGVServeSkidCtrlCmd: UGVServeSkidCtrlCmd,
  FaultInjection_Response: FaultInjection_Response,
  EgoNoisyStatus: EgoNoisyStatus,
  GripperState: GripperState,
  FaultInjection_Controller: FaultInjection_Controller,
  SetTrafficLight: SetTrafficLight,
  SyncModeAddObject: SyncModeAddObject,
  EgoDetailStatus: EgoDetailStatus,
  SyncModeScenarioLoad: SyncModeScenarioLoad,
  SaveSensorData: SaveSensorData,
  VehicleSpec: VehicleSpec,
  IntersectionStatus: IntersectionStatus,
  RadarDetections: RadarDetections,
  VelocityCmd: VelocityCmd,
  SensorPosControl: SensorPosControl,
  IntscnTL: IntscnTL,
  SyncModeRemoveObject: SyncModeRemoveObject,
  ShipState: ShipState,
  ObjectStatusExtended: ObjectStatusExtended,
  ObjectStatusList: ObjectStatusList,
  GVStateCmd: GVStateCmd,
  TOF: TOF,
  SyncModeCmd: SyncModeCmd,
  WaitForTick: WaitForTick,
  GVDirectCmd: GVDirectCmd,
  XYZ: XYZ,
  GhostMessage: GhostMessage,
  SkateboardCtrlCmd: SkateboardCtrlCmd,
  ScenarioLoad: ScenarioLoad,
  DillyCmdResponse: DillyCmdResponse,
  ObjectStatusListExtended: ObjectStatusListExtended,
  PRCtrlCmd: PRCtrlCmd,
  ReplayInfo: ReplayInfo,
  MultiEgoSetting: MultiEgoSetting,
  Lamps: Lamps,
  VehicleSpecIndex: VehicleSpecIndex,
  MultiPlayEventResponse: MultiPlayEventResponse,
  SkateboardStatus: SkateboardStatus,
  PREvent: PREvent,
  MoraiSrvResponse: MoraiSrvResponse,
  MSITCustomMessage: MSITCustomMessage,
  ObjectStatus: ObjectStatus,
  GetTrafficLightStatus: GetTrafficLightStatus,
  IntersectionControl: IntersectionControl,
  RobotOutput: RobotOutput,
  TrafficLight: TrafficLight,
  SyncModeInfo: SyncModeInfo,
  Obstacle: Obstacle,
  ManipulatorControl: ManipulatorControl,
  SkidSteer6wUGVCtrlCmd: SkidSteer6wUGVCtrlCmd,
  FaultInjection_Tire: FaultInjection_Tire,
  WoowaDillyStatus: WoowaDillyStatus,
  FaultInjection_Sensor: FaultInjection_Sensor,
  MoraiSimProcHandle: MoraiSimProcHandle,
  MapSpec: MapSpec,
  CMDConveyor: CMDConveyor,
  RobotPose: RobotPose,
  GPSMessage: GPSMessage,
  ENU: ENU,
  NpcGhostCmd: NpcGhostCmd,
  ERP42Info: ERP42Info,
  CollisionData: CollisionData,
  EgoVehicleStatus: EgoVehicleStatus,
  DdCtrlCmd: DdCtrlCmd,
  Transforms: Transforms,
  ShipCtrlCmd: ShipCtrlCmd,
  SyncModeResultResponse: SyncModeResultResponse,
  Competition: Competition,
  RobotState: RobotState,
  VehicleCollision: VehicleCollision,
  MapSpecIndex: MapSpecIndex,
  Obstacles: Obstacles,
  DillyCmd: DillyCmd,
  PRStatus: PRStatus,
  GeoVector3Message: GeoVector3Message,
  NpcGhostInfo: NpcGhostInfo,
};
