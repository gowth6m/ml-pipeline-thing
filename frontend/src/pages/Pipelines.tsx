
import { useNavigate } from "react-router-dom";
import { PipelineList } from "@/components/PipelineList";
import { Pipeline } from "@/types/pipeline";

const Pipelines = () => {
  const navigate = useNavigate();

  const handleSelectPipeline = (pipeline: Pipeline) => {
    navigate(`/pipeline/${pipeline.id}`, { state: { pipeline } });
  };

  const handleCreatePipeline = () => {
    navigate('/create-pipeline');
  };

  return (
    <PipelineList 
      onSelectPipeline={handleSelectPipeline}
      onCreatePipeline={handleCreatePipeline}
    />
  );
};

export default Pipelines;
