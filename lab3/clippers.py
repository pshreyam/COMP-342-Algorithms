import sys


class ClippingWindow:
    def __init__(self, xw_min, xw_max, yw_min, yw_max):
        self.xw_min = xw_min
        self.xw_max = xw_max
        self.yw_min = yw_min
        self.yw_max = yw_max

    def get_endpoints(self):
        return [
            (self.xw_min, self.yw_min),
            (self.xw_max, self.yw_min),
            (self.xw_max, self.yw_max),
            (self.xw_min, self.yw_max),
        ]

    def get_region_code(self, point):
        x, y = point
        region_code = [y > self.yw_max, y < self.yw_min, x > self.xw_max, x < self.xw_min]
        region_code = list(map(lambda x: 1 if x else 0, region_code))
        return region_code

    def cohen_sutherland_clip(self, start, end):
        x1, y1 = start
        x2, y2 = end

        rc_start = self.get_region_code(start)
        rc_end = self.get_region_code(end)

        rc_all_zero_start = all(x==0 for x in rc_start)
        rc_all_zero_end = all(x==0 for x in rc_end)

        if rc_all_zero_start and rc_all_zero_end:
            # The line is trivially accepted!
            return start, end

        result_anding_codes = [x & y for x, y in zip(rc_start, rc_end)]

        if not all(x==0 for x in result_anding_codes):
            # The line is trivially rejected!
            return False

        m = (y2 - y1) / (x2 - x1)

        if not rc_all_zero_start:
            rc_outside = rc_start
            other_point = end
        else:
            rc_outside = rc_end
            other_point = start

        if rc_outside[-1]:
            x = self.xw_min
            y = int(y1 + m * (x - x1))
            return self.cohen_sutherland_clip([x, y], other_point)
        if rc_outside[-2]:
            x = self.xw_min
            y = int(y1 + m * (x - x1))
            return self.cohen_sutherland_clip([x, y], other_point)
        if rc_outside[-3]:
            y = self.yw_min
            x = int(x1 + (y - y1) / m)
            return self.cohen_sutherland_clip([x, y], other_point)
        if rc_outside[-4]:
            y = self.yw_max
            x = int(x1 + (y - y1) / m)
            return self.cohen_sutherland_clip([x, y], other_point)

    def liang_barsky_clip(self, start, end):
        x1, y1 = start
        x2, y2 = end

        dx = x2 - x1
        dy = y2 - y1

        p = [-dx, dx, -dy, dy]
        q = [x1 - self.xw_min, self.xw_max - x1, y1 - self.yw_min, self.yw_max - y1]

        p_zero = [True if x==0 else False for x in p]
        q_negative = [True if x<0 else False for x in q]

        if any(x & y for x, y in zip(p_zero, q_negative)):
            # The line is trivially rejected!
            return False

        r = [y/x for x, y in zip(p, q)]

        negative_p = [True if x < 0 else False for x in p]

        max_r = [0,]
        min_r = [1,]

        for i, x in enumerate(r):
            if negative_p[i]:
                max_r.append(x)
            else:
                min_r.append(x)

        u1 = max(max_r)
        u2 = min(min_r)

        if u1 > u2:
            # The line is rejected!
            return False

        # The line is accepted!
        return [x1 + u1*dx, y1 + u1*dy], [x1 + u2*dx, y1 + u2*dy]

    def vertex_inside(self, vertex, clipper):
        x, y = vertex
        if clipper == "T":
            return y <= self.yw_max
        elif clipper == "B":
            return y >= self.yw_min
        elif clipper == "R":
            return x <= self.xw_max
        elif clipper == "L":
            return x >= self.xw_min

    def find_intersection(self, start, end, clipper):
        x1, y1 = start
        x2, y2 = end

        dy = y2 - y1
        dx = x2 - x1

        m = dy/dx if dx != 0 else sys.maxsize

        if clipper == "T":
            return round(x1 + (self.yw_max-y1)/m), self.yw_max
        elif clipper == "B":
            return round(x1 + (self.yw_min-y1)/m), self.yw_min
        elif clipper == "R":
            return self.xw_max, round(y1 + m * (self.xw_max - x1))
        elif clipper == "L":
            return self.xw_min, round(y1 + m * (self.xw_min - x1))

    def sutherland_hodgeman_clip(self, vertices):
        output_vertices = vertices[:]

        for clipper in "TBRL":
            vertices = output_vertices[:]
            output_vertices.clear()
            for i in range(len(vertices)):
                V1 = vertices[i-1]
                V2 = vertices[i]
                if (self.vertex_inside(V1, clipper) and not self.vertex_inside(V2, clipper)) or (not self.vertex_inside(V1, clipper) and self.vertex_inside(V2, clipper)):
                    intersection_point = self.find_intersection(V1, V2, clipper)
                    if not self.vertex_inside(V1, clipper) and self.vertex_inside(V2, clipper):
                        output_vertices.append(intersection_point)
                        output_vertices.append(V2)
                    elif not self.vertex_inside(V2, clipper) and self.vertex_inside(V1, clipper):
                        output_vertices.append(intersection_point)
                elif self.vertex_inside(V1, clipper) and self.vertex_inside(V2, clipper):
                    output_vertices.append(V2)
        return output_vertices
