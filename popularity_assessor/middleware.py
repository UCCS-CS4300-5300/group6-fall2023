import cProfile
import pstats
import io
from django.http import HttpResponse


class ProfilingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
            # if request contais popularity_assessor/profile
        if "/popularity_assessor/profile/" in request.path:
        
            # If 'profile' is present in the query parameters, enable profiling
            profiler = cProfile.Profile()
            response = profiler.runcall(self.get_response, request)
            profiler_data = io.StringIO()
            stats = pstats.Stats(profiler, stream=profiler_data)
            stats.sort_stats('cumulative')
            stats.print_stats()
            response.content = profiler_data.getvalue()
            with open('test.txt', 'w') as file:
                file.write(profiler_data.getvalue())
            return response

        return self.get_response(request)