from __future__ import annotations

from collections.abc import Callable

import graphql


class Qlot:
    def __init__(self) -> None:
        self._query: dict[str, graphql.GraphQLField] = {}
        self._mutation: dict[str, graphql.GraphQLField] = {}
        self._subscription: dict[str, graphql.GraphQLField] = {}

    def query[**P, R](self, name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def _query(func: Callable[P, R]) -> Callable[P, R]:
            self._query[name] = graphql.GraphQLField(
                graphql.GraphQLString,
                resolve=lambda obj, info: func(),
            )
            return func

        return _query

    def mutation[**P, R](self, name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def _mutation(func: Callable[P, R]) -> Callable[P, R]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return func(*args, **kwargs)

            return wrapper

        return _mutation

    def subscription[
        **P,
        R,
    ](self, name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def _subscription(func: Callable[P, R]) -> Callable[P, R]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return func(*args, **kwargs)

            return wrapper

        return _subscription

    @property
    def schema(self) -> graphql.GraphQLSchema:
        return graphql.GraphQLSchema(
            query=graphql.GraphQLObjectType(
                name="Query",
                fields=self._query,
            ),
        )

    def execute(self, query: str) -> graphql.ExecutionResult:
        return graphql.graphql_sync(self.schema, query)
