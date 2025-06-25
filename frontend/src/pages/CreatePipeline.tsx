
import { useNavigate } from "react-router-dom";
import { CreatePipeline as CreatePipelineComponent } from "@/components/CreatePipeline";
import { Pipeline } from "@/types/pipeline";

const CreatePipeline = () => {
  const navigate = useNavigate();

  const handlePipelineCreated = (pipeline: Pipeline) => {
    navigate(`/pipeline/${pipeline.id}`, { state: { pipeline } });
  };

  const handleCancel = () => {
    navigate('/pipelines');
  };

  return (
    <CreatePipelineComponent
      onPipelineCreated={handlePipelineCreated}
      onCancel={handleCancel}
    />
  );
};

export default CreatePipeline;
