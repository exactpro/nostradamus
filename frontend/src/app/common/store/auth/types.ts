import { HttpStatus } from "app/common/types/http.types";
import { User } from "app/common/types/user.types";

export interface AuthStore {
	status: HttpStatus;
	user: User | null;
}
