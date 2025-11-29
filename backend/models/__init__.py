"""Database models package"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .project import Project
from .page import Page
from .task import Task

__all__ = ['db', 'Project', 'Page', 'Task']

