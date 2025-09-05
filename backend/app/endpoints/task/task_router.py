from app.models.tasks.task_model import Task
from app.controller.base_controller import BaseController
from app.controller.auth import authentication
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from app.endpoints.base.base_router import BaseRouter
from app.models.users.user import User
from app.endpoints.base.pagination import PaginationResponse, PaginationInput
from sqlmodel import select, func


class CreateTask(BaseModel):
    title: str
    description: str | None = None


class UpdateTask(CreateTask):
    completed: bool | None = None


class AnalyticsResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int


class TaskRouter(BaseRouter[Task, CreateTask]):
    def __init__(self):
        super().__init__(
            prefix="/tasks",
            tag=["tasks"],
            controller=BaseController(Task),
            model=Task,
            create_type=CreateTask,
            auth_object=[Depends(authentication.get_current_user)],
        )

    def setup_routes(self):
        self.router.add_api_route(
            "/analytics",
            self.analytics,
            methods=["GET"],
            response_model=AnalyticsResponse,
            description="Get task analytics",
            summary="Task Analytics",
        )
        return super().setup_routes()

    async def read_all(
        self,
        pagination: PaginationInput = Depends(),
        user: User = Depends(authentication.get_current_user),
    ) -> PaginationResponse[Task]:
        offset = (pagination.page - 1) * pagination.per_page
        query = select(self.model).where(self.model.user_id == user.id)
        total = self.controller.session.exec(
            select(func.count()).select_from(query)  # type: ignore
        ).one()
        data = self.controller.session.exec(
            query.offset(offset).limit(pagination.per_page)
        ).all()
        return PaginationResponse[Task](
            data=data,
            total=total,
            page=pagination.page,
            per_page=pagination.per_page,
            total_pages=(
                total // pagination.per_page
                + (1 if total % pagination.per_page > 0 else 0)
            ),
        )

    async def update(  # type: ignore
        self,
        id: int,
        data: UpdateTask,
        user: User = Depends(authentication.get_current_user),
    ) -> Task:
        try:
            old_task = self.controller.session.exec(
                select(Task).where(Task.id == id).where(Task.user_id == user.id)
            ).first()
            if not old_task:
                raise HTTPException(status_code=404, detail="Task not found")
            old_task.title = data.title
            old_task.description = data.description
            old_task.completed = (
                data.completed if data.completed is not None else old_task.completed
            )
            self.controller.session.add(old_task)
            self.controller.session.commit()
            self.controller.session.refresh(old_task)
            return old_task
        except Exception as e:
            self.controller.session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Error updating task: {str(e)}"
            )

    async def create(  # type: ignore
        self,
        data: CreateTask,
        user: User = Depends(authentication.get_current_user),
    ) -> Task | bool:
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user")
        new_task = await self.controller.create(
            data=Task(
                **data.model_dump(),
                user_id=user.id,
            ),
        )
        if not new_task:
            raise HTTPException(status_code=400, detail="Task creation failed")
        return new_task

    async def analytics(
        self,
        user: User = Depends(authentication.get_current_user),
    ) -> AnalyticsResponse:
        base_query = select(func.count()).where(Task.user_id == user.id)
        total_tasks = self.controller.session.exec(base_query).one()
        completed_tasks = self.controller.session.exec(
            base_query.where(Task.completed)  # type: ignore
        ).one()
        pending_tasks = total_tasks - completed_tasks

        return AnalyticsResponse(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
        )


task_router = TaskRouter()
