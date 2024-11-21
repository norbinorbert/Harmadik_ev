package edu.bbte.bnim2219.server.dao.memory;

import edu.bbte.bnim2219.server.dao.TrainingDao;
import edu.bbte.bnim2219.server.model.Training;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collection;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class TrainingInMemDao implements TrainingDao {
    private final Map<Long, Training> trainings = new ConcurrentHashMap<>();
    private final Logger log = LoggerFactory.getLogger(TrainingInMemDao.class);

    @Override
    public void create(Training training) {
        if (trainings.get(training.getTrainingId()) != null) {
            log.error("Training added");
            return;
        }
        Training training1 = new Training(training.getTrainingId(), training.getDuration(), training.getComplete());
        trainings.put(training1.getTrainingId(), training1);
    }

    @Override
    public Training findById(Long id) {
        return trainings.get(id);
    }

    @Override
    public Collection<Training> findAll() {
        return trainings.values();
    }
}
