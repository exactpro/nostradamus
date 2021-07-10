import { HttpStatus } from "app/common/types/http.types";

export const setTrainingStatus = (status: HttpStatus) =>
  ({
    type: "SET_TRAINING_STATUS",
    status,
  } as const);
