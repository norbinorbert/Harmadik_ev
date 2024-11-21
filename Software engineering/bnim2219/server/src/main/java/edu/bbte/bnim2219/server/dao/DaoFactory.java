package edu.bbte.bnim2219.server.dao;

import edu.bbte.bnim2219.server.dao.memory.MemoryDaoFactory;

public abstract class DaoFactory {
    private static DaoFactory instance;

    public static synchronized DaoFactory getInstance() {
        if (instance == null) {
            instance = new MemoryDaoFactory();
        }
        return instance;
    }

    public abstract TrainingDao getTrainingDao();
}
