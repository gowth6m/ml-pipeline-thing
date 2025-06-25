/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** TriggerType */
export enum TriggerType {
  MANUAL = "MANUAL",
  SCHEDULED = "SCHEDULED",
  API = "API",
  WEBHOOK = "WEBHOOK",
}

/** StageType */
export enum StageType {
  DATA_INGESTION = "DATA_INGESTION",
  DATA_VALIDATION = "DATA_VALIDATION",
  DATA_PREPROCESSING = "DATA_PREPROCESSING",
  FEATURE_ENGINEERING = "FEATURE_ENGINEERING",
  DATA_SPLITTING = "DATA_SPLITTING",
  MODEL_TRAINING = "MODEL_TRAINING",
  MODEL_VALIDATION = "MODEL_VALIDATION",
  MODEL_EVALUATION = "MODEL_EVALUATION",
  MODEL_TESTING = "MODEL_TESTING",
  MODEL_REGISTRATION = "MODEL_REGISTRATION",
  MODEL_DEPLOYMENT = "MODEL_DEPLOYMENT",
  MODEL_MONITORING = "MODEL_MONITORING",
  EXPLORATORY_DATA_ANALYSIS = "EXPLORATORY_DATA_ANALYSIS",
  HYPERPARAMETER_TUNING = "HYPERPARAMETER_TUNING",
  MODEL_COMPARISON = "MODEL_COMPARISON",
  ENVIRONMENT_SETUP = "ENVIRONMENT_SETUP",
  RESOURCE_PROVISIONING = "RESOURCE_PROVISIONING",
  CLEANUP = "CLEANUP",
  CUSTOM = "CUSTOM",
}

/** StageStatus */
export enum StageStatus {
  PENDING = "PENDING",
  RUNNING = "RUNNING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED",
  SKIPPED = "SKIPPED",
}

/** RunStatus */
export enum RunStatus {
  PENDING = "PENDING",
  RUNNING = "RUNNING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED",
  CANCELLED = "CANCELLED",
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/**
 * HealthCheck
 * Health check response model
 */
export interface HealthCheck {
  /**
   * Status
   * @default "healthy"
   */
  status?: string;
  /** Version */
  version: string;
  /**
   * Database
   * @default "connected"
   */
  database?: string;
  /** Uptime */
  uptime: number;
  /** Environment */
  environment: string;
  /**
   * Timestamp
   * @format date-time
   */
  timestamp: string;
  /** Memory usage model */
  memoryUsage: MemoryUsage;
}

/**
 * MemoryUsage
 * Memory usage model
 */
export interface MemoryUsage {
  /** Used */
  used: string;
  /** Available */
  available: string;
  /** Percent */
  percent: string;
}

/** PaginationResponse[PipelineResponse] */
export interface PaginationResponsePipelineResponse {
  /**
   * Items
   * List of items for the current page
   */
  items: PipelineResponse[];
  /**
   * Total
   * Total number of items across all pages
   */
  total: number;
  /**
   * Page
   * Current page number (1-based)
   */
  page: number;
  /**
   * Size
   * Number of items per page
   */
  size: number;
  /**
   * Pages
   * Total number of pages
   */
  pages: number;
  /**
   * Hasnext
   * Whether there is a next page
   */
  hasNext: boolean;
  /**
   * Hasprev
   * Whether there is a previous page
   */
  hasPrev: boolean;
}

/** PaginationResponse[PipelineRunResponse] */
export interface PaginationResponsePipelineRunResponse {
  /**
   * Items
   * List of items for the current page
   */
  items: PipelineRunResponse[];
  /**
   * Total
   * Total number of items across all pages
   */
  total: number;
  /**
   * Page
   * Current page number (1-based)
   */
  page: number;
  /**
   * Size
   * Number of items per page
   */
  size: number;
  /**
   * Pages
   * Total number of pages
   */
  pages: number;
  /**
   * Hasnext
   * Whether there is a next page
   */
  hasNext: boolean;
  /**
   * Hasprev
   * Whether there is a previous page
   */
  hasPrev: boolean;
}

/** PipelineCreate */
export interface PipelineCreate {
  /**
   * Name
   * @minLength 1
   * @maxLength 255
   */
  name: string;
  /** Description */
  description?: string | null;
  /** Config */
  config?: Record<string, any> | null;
  /**
   * Stages
   * @minItems 1
   */
  stages: PipelineStageCreate[];
}

/** PipelineResponse */
export interface PipelineResponse {
  /** Id */
  id: string;
  /** Name */
  name: string;
  /** Description */
  description?: string | null;
  /** Status */
  status: string;
  /** Config */
  config?: Record<string, any> | null;
  /** Startedat */
  startedAt?: string | null;
  /** Completedat */
  completedAt?: string | null;
  /** Executiontime */
  executionTime?: number | null;
  /** Memoryusage */
  memoryUsage?: number | null;
  /** Cpuusage */
  cpuUsage?: number | null;
  /**
   * Createdat
   * @format date-time
   */
  createdAt: string;
  /**
   * Updatedat
   * @format date-time
   */
  updatedAt: string;
}

/** PipelineRunResponse */
export interface PipelineRunResponse {
  /** Id */
  id: string;
  /** Pipelineid */
  pipelineId: string;
  status: RunStatus;
  triggerType: TriggerType;
  /** Triggeredby */
  triggeredBy?: string | null;
  /** Startedat */
  startedAt?: string | null;
  /** Completedat */
  completedAt?: string | null;
  /** Executiontime */
  executionTime?: number | null;
  /** Runconfig */
  runConfig?: Record<string, any> | null;
  /** Environment */
  environment: string;
  /** Maxmemoryusage */
  maxMemoryUsage?: number | null;
  /** Maxcpuusage */
  maxCpuUsage?: number | null;
  /**
   * Successcount
   * @default 0
   */
  successCount?: number;
  /**
   * Failedcount
   * @default 0
   */
  failedCount?: number;
  /** Errormessage */
  errorMessage?: string | null;
  /** Outputdata */
  outputData?: Record<string, any> | null;
  /** Tags */
  tags?: string[] | null;
  /** Notes */
  notes?: string | null;
  /**
   * Createdat
   * @format date-time
   */
  createdAt: string;
  /**
   * Updatedat
   * @format date-time
   */
  updatedAt: string;
}

/** PipelineRunWithStages */
export interface PipelineRunWithStages {
  /** Id */
  id: string;
  /** Pipelineid */
  pipelineId: string;
  status: RunStatus;
  triggerType: TriggerType;
  /** Triggeredby */
  triggeredBy?: string | null;
  /** Startedat */
  startedAt?: string | null;
  /** Completedat */
  completedAt?: string | null;
  /** Executiontime */
  executionTime?: number | null;
  /** Runconfig */
  runConfig?: Record<string, any> | null;
  /** Environment */
  environment: string;
  /** Maxmemoryusage */
  maxMemoryUsage?: number | null;
  /** Maxcpuusage */
  maxCpuUsage?: number | null;
  /**
   * Successcount
   * @default 0
   */
  successCount?: number;
  /**
   * Failedcount
   * @default 0
   */
  failedCount?: number;
  /** Errormessage */
  errorMessage?: string | null;
  /** Outputdata */
  outputData?: Record<string, any> | null;
  /** Tags */
  tags?: string[] | null;
  /** Notes */
  notes?: string | null;
  /**
   * Createdat
   * @format date-time
   */
  createdAt: string;
  /**
   * Updatedat
   * @format date-time
   */
  updatedAt: string;
  /**
   * Stageruns
   * @default []
   */
  stageRuns?: StageRunResponse[];
}

/** PipelineStageCreate */
export interface PipelineStageCreate {
  /**
   * Name
   * @minLength 1
   * @maxLength 255
   */
  name: string;
  stageType: StageType;
  /** Customname */
  customName?: string | null;
  /**
   * Order
   * @min 0
   */
  order: number;
  /** Config */
  config?: Record<string, any> | null;
  /** Dependencies */
  dependencies?: string[] | null;
}

/** PipelineStageResponse */
export interface PipelineStageResponse {
  /** Id */
  id: string;
  /** Name */
  name: string;
  stageType: StageType;
  /** Customname */
  customName?: string | null;
  status: StageStatus;
  /** Order */
  order: number;
  /** Config */
  config?: Record<string, any> | null;
  /** Dependencies */
  dependencies?: string[] | null;
  /** Startedat */
  startedAt?: string | null;
  /** Completedat */
  completedAt?: string | null;
  /** Executiontime */
  executionTime?: number | null;
  /** Outputpath */
  outputPath?: string | null;
  /** Metrics */
  metrics?: Record<string, any> | null;
  /**
   * Createdat
   * @format date-time
   */
  createdAt: string;
  /**
   * Updatedat
   * @format date-time
   */
  updatedAt: string;
}

/** PipelineWithStages */
export interface PipelineWithStages {
  /** Id */
  id: string;
  /** Name */
  name: string;
  /** Description */
  description?: string | null;
  /** Status */
  status: string;
  /** Config */
  config?: Record<string, any> | null;
  /** Startedat */
  startedAt?: string | null;
  /** Completedat */
  completedAt?: string | null;
  /** Executiontime */
  executionTime?: number | null;
  /** Memoryusage */
  memoryUsage?: number | null;
  /** Cpuusage */
  cpuUsage?: number | null;
  /**
   * Createdat
   * @format date-time
   */
  createdAt: string;
  /**
   * Updatedat
   * @format date-time
   */
  updatedAt: string;
  /**
   * Stages
   * @default []
   */
  stages?: PipelineStageResponse[];
}

/** StageRunResponse */
export interface StageRunResponse {
  /** Id */
  id: string;
  /** Pipelinerunid */
  pipelineRunId: string;
  /** Stageid */
  stageId: string;
  status: RunStatus;
  /**
   * Attemptnumber
   * @default 1
   */
  attemptNumber?: number;
  /** Startedat */
  startedAt?: string | null;
  /** Completedat */
  completedAt?: string | null;
  /** Executiontime */
  executionTime?: number | null;
  /** Memoryusage */
  memoryUsage?: number | null;
  /** Cpuusage */
  cpuUsage?: number | null;
  /** Outputdata */
  outputData?: Record<string, any> | null;
  /** Errormessage */
  errorMessage?: string | null;
  /** Logs */
  logs?: string | null;
  /**
   * Createdat
   * @format date-time
   */
  createdAt: string;
  /**
   * Updatedat
   * @format date-time
   */
  updatedAt: string;
}

/** TriggerRunRequest */
export interface TriggerRunRequest {
  /** Runconfig */
  runConfig?: Record<string, any> | null;
  /**
   * Environment
   * @default "development"
   * @pattern ^(development|staging|production)$
   */
  environment?: string;
  /** Triggeredby */
  triggeredBy?: string | null;
  /** Tags */
  tags?: string[] | null;
  /** Notes */
  notes?: string | null;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}
