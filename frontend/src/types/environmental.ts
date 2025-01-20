/**
 * Environmental configuration types
 */

export interface EnvironmentConfig {
  API_URL: string;
  NODE_ENV: "development" | "production" | "test";
  DEBUG: boolean;
}

export type EnvVarKey = keyof EnvironmentConfig;
