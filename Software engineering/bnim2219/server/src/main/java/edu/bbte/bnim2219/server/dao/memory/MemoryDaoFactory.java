package edu.bbte.bnim2219.server.dao.memory;

import edu.bbte.bnim2219.server.dao.TrainingDao;
import edu.bbte.bnim2219.server.dao.DaoFactory;

public class MemoryDaoFactory extends DaoFactory {

    @Override
    public TrainingDao getTrainingDao() {
        return new TrainingInMemDao();
    }
}
