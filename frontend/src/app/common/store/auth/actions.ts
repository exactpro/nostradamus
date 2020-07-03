import { removeData } from 'app/common/functions/local-storage';
import {Team, User} from "app/common/types/user.types";
import {HttpStatus} from "app/common/types/http.types";

export const setUser = (user: User) => ({
  type: 'ACTION_AUTH_SET_USER',
  user
} as const);

export const deleteUser = () => {
  removeData('user');

  return ({
    type: 'ACTION_AUTH_DELETE_USER',
  } as const)
};

export const setStatus = (status: HttpStatus) => ({
  type: 'ACTION_AUTH_SET_STATUS',
  status
} as const);

export const setTeamList = (teamList: Team[]) => ({
  type: 'ACTION_AUTH_SET_TEAM_LIST',
  teamList
} as const);
