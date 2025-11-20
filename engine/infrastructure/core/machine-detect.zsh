#!/usr/bin/env zsh
# VIRENS Machine Detection
# Determines if current machine is hub or workstation

virens_machine_role() {
    # Returns 'hub' or 'workstation'
    local user_dir=$(virens_user)
    local machine_config="$user_dir/config/machine.yaml"
    
    if [ -f "$machine_config" ]; then
        grep "^role:" "$machine_config" | awk '{print $2}'
    else
        echo "workstation"  # Default
    fi
}

virens_machine_name() {
    # Returns machine name (archive, conservatory, estuary, etc.)
    local user_dir=$(virens_user)
    local machine_config="$user_dir/config/machine.yaml"
    
    if [ -f "$machine_config" ]; then
        grep "^name:" "$machine_config" | awk '{print $2}'
    else
        scutil --get ComputerName
    fi
}

virens_is_hub() {
    # Returns 0 (true) if hub, 1 (false) if workstation
    [ "$(virens_machine_role)" = "hub" ]
}

# Conditional loading based on machine role
virens_load_machine_config() {
    if virens_is_hub; then
        log_info "Running on hub machine: $(virens_machine_name)"
        # Hub-specific configurations here
    else
        log_info "Running on workstation: $(virens_machine_name)"
        # Workstation-specific configurations here
    fi
}
