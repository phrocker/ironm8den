"""
GraphQL Workout types
"""

import graphene
from django.utils import timezone
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from workouts.models import MuscleGroup, Workout

from .helpers import get_object


class MuscleGroupType(DjangoObjectType):
    class Meta:
        model = MuscleGroup


class WorkoutStatusesEnum(graphene.Enum):
    PENDING = Workout.PENDING
    IN_PROGRESS = Workout.IN_PROGRESS
    CANCELLED = Workout.CANCELLED
    COMPLETE = Workout.COMPLETE


class WorkoutFieldInputType(graphene.InputObjectType):
    date_started = graphene.types.datetime.DateTime()
    date_ended = graphene.types.datetime.DateTime()
    status = graphene.Field(WorkoutStatusesEnum)


class WorkoutType(DjangoObjectType):
    exercise_count = graphene.Int()

    class Meta:
        model = Workout

    @staticmethod
    def resolve_exercise_count(workout, info):
        return workout.exercises.count()


class CreateWorkout(graphene.Mutation):
    workout = graphene.Field(WorkoutType)

    @staticmethod
    def mutate(_, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not authenticated.")

        new_workout = Workout.objects.create(user=user, date_started=timezone.now())

        return CreateWorkout(workout=new_workout)


class RemoveWorkout(graphene.Mutation):
    workout = graphene.Field(WorkoutType)

    class Arguments:
        workout_id = graphene.Int(required=True)

    @staticmethod
    def mutate(_, info, workout_id):
        user = info.context.user

        workout = get_object(Workout, {"id": workout_id, "user": user.id})
        workout.updated_at = timezone.now()
        workout.is_active = False
        workout.save()

        return RemoveWorkout(workout=workout)


class UpdateWorkout(graphene.Mutation):
    workout = graphene.Field(WorkoutType)

    class Arguments:
        workout_id = graphene.Int(required=True)
        workout_fields = graphene.Argument(WorkoutFieldInputType, required=True)

    @staticmethod
    def mutate(_, info, workout_id, workout_fields):
        user = info.context.user
        workout = get_object(Workout, {"id": workout_id, "user": user.id})

        dirty = False
        # Unpack the fields and update the model
        for name, value in workout_fields.items():
            if not hasattr(workout, name):
                continue

            setattr(workout, name, value)
            dirty = True

        if dirty:
            workout.updated_at = timezone.now()
            workout.save()

        return UpdateWorkout(workout=workout)
