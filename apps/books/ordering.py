"""
Custom ordering filter that translates _asc/_desc to Django format.
"""
from rest_framework.filters import OrderingFilter


class CustomOrderingFilter(OrderingFilter):
    """
    Ordering filter that accepts clear _asc and _desc suffixes.
    
    Example:
    - title_asc → title (ascending)
    - title_desc → -title (descending)
    """
    
    ordering_param = 'ordering'
    
    def get_ordering(self, request, queryset, view):
        """Convert _asc/_desc format to Django ordering format."""
        params = request.query_params.get(self.ordering_param)
        
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = []
            
            for field in fields:
                if field.endswith('_desc'):
                    # Convert field_desc to -field
                    ordering.append('-' + field[:-5])
                elif field.endswith('_asc'):
                    # Convert field_asc to field
                    ordering.append(field[:-4])
                else:
                    # Pass through unchanged (support both formats)
                    ordering.append(field)
            
            # Validate against allowed fields
            valid_fields = getattr(view, 'ordering_fields', None)
            if valid_fields:
                ordering = [
                    field for field in ordering
                    if field.lstrip('-') in valid_fields
                ]
            
            if ordering:
                return ordering
        
        # Return default ordering
        return self.get_default_ordering(view)
