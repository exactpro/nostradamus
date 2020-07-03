/**
 * Types of user roles
 */
export enum UserRole {
  QA = 'QA'
}

/**
 * Model of user data for authentication
 */
export interface UserSignIn {
  credentials: string,
  password: string
}

/**
 * Model of user data for registration
 */
export interface UserSignUp {
  team: number | null,
  email: string,
  name: string,
  password: string
}

/**
 * Main user model
 */
export interface User {
  id: number;
  name: string;
  email: string;
  team: string; // team name, not id
  role: UserRole; // role name, not id
  token: string;
}

/**
 * Main team model
 */
export interface Team {
  id: number;
  name: string;
}
