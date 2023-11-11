def get_router_by_id(routers_table, id):
    for router in routers_table:
        if router.id == id:
            return router