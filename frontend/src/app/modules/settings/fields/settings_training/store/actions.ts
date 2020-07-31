import { TrainingActionTypes, TrainingSubSection } from "./types"
import { HttpStatus } from "app/common/types/http.types"

export const setSettingsTrainingData = (data: any, section: TrainingSubSection) =>
({
    data,
    section,
    type: TrainingActionTypes.setSettingsTrainingData
}  as const) 

export const setSettingsTrainingStatus = (status: HttpStatus, section: TrainingSubSection ) =>
({
    section,
    status,
    type: TrainingActionTypes.setSettingsTrainingStatus,
}  as const) 

export const clearSettingsTrainingData = () => ({ type: TrainingActionTypes.clearSettingsTrainingData } as const) 
