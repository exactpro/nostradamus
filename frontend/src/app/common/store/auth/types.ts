import {HttpStatus} from "app/common/types/http.types";
import {Team, User} from "app/common/types/user.types";

export interface AuthStore {
  status: HttpStatus,
  user: User | null,
  teamList: Team[]
}