
import { 
  PipelineWithStages, 
  PipelineStageResponse, 
  PipelineRunWithStages 
} from './index';

export type Pipeline = PipelineWithStages;

export interface PipelineStep extends PipelineStageResponse {
  command?: string;
  parameters?: Record<string, unknown>;
}

export interface PipelineRun extends PipelineRunWithStages {
  pipeline_id: string;
  started_at: string;
  completed_at?: string;
  metadata?: Record<string, unknown>;
}
